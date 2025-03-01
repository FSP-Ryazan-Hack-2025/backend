from typing import List

from src.products.exceptions import NotFoundException, AccessException
from src.products.models import Product
from src.products.repositories import ProductRepository
from src.products.schemas import ProductCreate, ProductEdit
from src.users.models import Seller


class CategoryService:
    repository = ProductRepository()

    async def get_product_by_id(self, product_id: int) -> Product:
        return await self.repository.get_product_by_id(product_id)

    def validate_product(self, product: Product, seller_inn: int) -> bool:
        if product is None:
            raise NotFoundException

        if product.seller_inn != seller_inn:
            raise AccessException

        return True

    async def create_product(self, product: ProductCreate, seller_inn: int) -> Product:
        return await self.repository.create_product(product, seller_inn)

    async def edit_product(self, product_edit: ProductEdit, product_id: int, seller: Seller) -> Product:
        product = await self.get_product_by_id(product_id)
        self.validate_product(product, seller.inn)

        return await self.repository.edit_product(product_edit, product.id)

    async def delete_product_by_id(self, product_id: int, seller: Seller):
        product = await self.get_product_by_id(product_id)
        self.validate_product(product, seller.inn)

        return self.repository.delete_product_by_id(product_id)
