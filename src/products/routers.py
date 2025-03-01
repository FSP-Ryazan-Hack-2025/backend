from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, UploadFile, Query

from src.products.models import ProductCategory
from src.products.schemas import ProductResponse, ProductCreate, ProductEdit
from src.products.services import ProductService
from src.users.models import User, Seller
from src.users.schemas import UserCreate, Token, UserResponse, SuccessfulResponse, UserEdit, \
    SuccessfulGetVerifyCodeResponse, SuccessfulValidation, SellerCreate, SellerResponse
from src.users.services import UserService

router = APIRouter(tags=["product"], prefix="/product")


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_by_id(
        product_id: int
) -> ProductResponse:
    product = await ProductService().get_product_by_id(product_id)
    return ProductResponse(**product.to_dict())


@router.get("/", response_model=List[ProductResponse])
async def get_products(
        category: Optional[ProductCategory] = Query(None, description="select optional product category")
) -> List[ProductResponse]:
    if category is None:
        products = await ProductService().get_all_products()
    else:
        products = await ProductService().get_all_products_by_category(category)

    return list(map(lambda x: ProductResponse(**x.to_dict()), products))


@router.post("/", response_model=ProductResponse)
async def create_product(
        current_seller: Annotated[Seller, Depends(UserService().get_current_seller)],
        new_product: ProductCreate
) -> ProductResponse:
    product = await ProductService().create_product(new_product, current_seller.inn)
    return ProductResponse(**product.to_dict())


@router.put("/{product_id}", response_model=ProductResponse)
async def edit_product(
        current_seller: Annotated[Seller, Depends(UserService().get_current_seller)],
        product_id: int,
        edited_product: ProductEdit
) -> ProductResponse:
    upd_product = await ProductService().edit_product(edited_product, product_id, current_seller)
    return ProductResponse(**upd_product.to_dict())


@router.delete("/{category_id}", response_model=SuccessfulResponse)
async def delete_product(
        current_seller: Annotated[Seller, Depends(UserService().get_current_seller)],
        product_id: int
) -> SuccessfulResponse:
    await ProductService().delete_product_by_id(product_id, current_seller)
    return SuccessfulResponse()
