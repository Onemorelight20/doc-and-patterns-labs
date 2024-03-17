from fastapi import Depends, HTTPException, APIRouter, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.data.schemas.digital_product import DigitalProduct, DigitalProductCreate
from app.data.repositories.digital_product import DigitalProductRepository

router = APIRouter(prefix="/digital_products", tags=["digital_products"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/create")
async def show_create_digital_product_form(request: Request):
    return templates.TemplateResponse("create_digital_product.html", {"request": request})


@router.post("/create")
async def create_digital_product(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    name = form.get("name")
    description = form.get("description")
    price = form.get("price")
    encryption_key = form.get("encryption_key")

    product_data = DigitalProductCreate(name=name, description=description, price=price, encryption_key=encryption_key)

    db_product = DigitalProductRepository.get_by_name(db, name=name)
    if db_product:
        raise HTTPException(status_code=400, detail="Product already exists. Please update the product name.")

    created_product = DigitalProductRepository.create(db=db, entity=product_data)
    return RedirectResponse(url=f"/digital_products/{created_product.id}?message=Product%20created%20successfully", status_code=303)


@router.get("/", response_model=list[DigitalProduct])
async def read_all_digital_products(
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size
    products = DigitalProductRepository.get_all(db, skip=skip, limit=page_size)
    
    total_products = DigitalProductRepository.get_total(db)
    total_pages = (total_products + page_size - 1) // page_size
    
    return templates.TemplateResponse(
        "digital_products.html",
        {"request": request, "products": products, "total_pages": total_pages, "current_page": page}
    )


@router.get("/{product_id}", response_model=DigitalProduct)
async def read_digital_product_by_id(request: Request, product_id: int, db: Session = Depends(get_db)):
    db_product = DigitalProductRepository.get_by_id(db, id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    message = request.query_params.get("message", None)

    return templates.TemplateResponse("digital_product.html", {"request": request, "product": db_product, "message": message})


@router.get("/update/{product_id}")
async def update_digital_product(request: Request, 
                                 product_id: int, 
                                 db: Session = Depends(get_db)):
    db_product = DigitalProductRepository.get_by_id(db, id=product_id)

    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse("update_digital_product.html", {"request": request, "product": db_product})


@router.post("/update/{product_id}")
async def update_digital_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    form = await request.form()
    name = form.get("name")
    description = form.get("description")
    price = form.get("price")
    encryption_key = form.get("encryption_key")

    product_data = DigitalProductCreate(name=name, description=description, price=price, encryption_key=encryption_key)

    db_product = DigitalProductRepository.get_by_id(db, id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    updated_product = DigitalProductRepository.update(db=db, id=product_id, entity=product_data)
    
    redirect_url = f"/digital_products/{product_id}?message=Product {updated_product.name} has been updated successfully"
    return RedirectResponse(url=redirect_url, status_code=303)


@router.post("/delete/{product_id}", response_model=DigitalProduct)
async def delete_digital_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    db_product = DigitalProductRepository.delete(db, id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse("deleted_product.html", {"request": request, "product": db_product})
