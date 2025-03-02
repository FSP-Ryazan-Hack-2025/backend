import os
import shutil
from pathlib import Path
from typing import List

from fastapi import UploadFile

from src.products.exceptions import NotFoundException, AccessException, ErrorLoadImageException
from src.products.models import Product, ProductCategory
from src.products.repositories import ProductRepository
from src.products.schemas import ProductCreate, ProductEdit
from src.users.exceptions import ErrorDeleteAvatarException
from src.users.models import Seller
from src.users.schemas import SuccessfulResponse


class ProductService:
    repository = ProductRepository()

    async def add_image(self, avatar: UploadFile, seller: Seller, product_id: int) -> SuccessfulResponse:

        product = await self.get_product_by_id(product_id)
        if product.seller_inn != seller.inn:
            raise AccessException()

        root = Path(__file__).parent.parent.parent
        image_path = os.path.join(root, "assets", "product_images", f"{product_id}.webp")

        try:
            with open(image_path, "wb+") as avatar_obj:
                shutil.copyfileobj(avatar.file, avatar_obj)
        except Exception as e:
            print("Error loading avatar:", e)
            raise ErrorLoadImageException()

        return SuccessfulResponse()

    async def get_image_url(self, product_id: int) -> str:
        return f"static/product_images/{product_id}.webp"

    async def delete_image(self, seller: Seller, product_id: int) -> SuccessfulResponse:

        product = await self.get_product_by_id(product_id)
        if product.seller_inn != seller.inn:
            raise AccessException()

        root = Path(__file__).parent.parent.parent
        image_path = os.path.join(root, "assets", "product_images", f"{product_id}.webp")

        try:
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            print("Error deleting avatar:", e)
            raise ErrorDeleteAvatarException()

        return SuccessfulResponse()

    async def get_product_by_id(self, product_id: int) -> Product:
        product = await self.repository.get_product_by_id(product_id)
        if product is None:
            raise NotFoundException()

        return product

    def validate_product(self, product: Product, seller_inn: int) -> bool:
        if product is None:
            raise NotFoundException

        if product.seller_inn != seller_inn:
            raise AccessException

        return True

    async def get_all_products(self) -> List[Product]:
        return await self.repository.get_all_products()

    async def get_all_products_by_category(self, category: ProductCategory) -> List[Product]:
        return await self.repository.get_all_products_by_category(category)

    async def create_product(self, product: ProductCreate, seller_inn: int) -> Product:
        return await self.repository.create_product(product, seller_inn)

    async def update_product_count(self, product_id: int, new_count: int) -> Product:
        return await self.repository.update_product_count(product_id, new_count)

    async def edit_product(self, product_edit: ProductEdit, product_id: int, seller: Seller) -> Product:
        product = await self.get_product_by_id(product_id)
        self.validate_product(product, seller.inn)

        return await self.repository.edit_product(product_edit, product.id)

    async def delete_product_by_id(self, product_id: int, seller: Seller):
        product = await self.get_product_by_id(product_id)
        self.validate_product(product, seller.inn)

        return await self.repository.delete_product_by_id(product_id)
