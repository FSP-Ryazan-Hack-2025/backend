import random
from typing import Optional, List

from sqlalchemy import insert, select, delete, update

from config_data.config import Config, load_config
from src.products.exceptions import AccessException, NotFoundException
from src.products.models import Product, ProductCategory
from src.products.schemas import ProductCreate, ProductEdit
from utils import auth_settings
from src.database import async_session

settings: Config = load_config(".env")
global_vars = settings.variablesData


class ProductRepository:
    async def generate_id(self) -> int:
        unique_id = random.randint(global_vars.MIN_ID, global_vars.MAX_ID)
        while await self.get_product_by_id(unique_id):
            unique_id = random.randint(global_vars.MIN_ID, global_vars.MAX_ID)

        return unique_id

    async def get_all_products(self) -> List[Product]:
        async with async_session() as session:
            query = select(Product)
            result = await session.execute(query)
            products = result.scalars().all()

        return products

    async def get_all_products_by_category(self, category: ProductCategory) -> List[Product]:
        async with async_session() as session:
            query = select(Product).where(Product.category == category)
            result = await session.execute(query)
            products = result.scalars().all()

        return products

    async def get_product_by_id(self, product_id: int) -> Product:
        async with async_session() as session:
            query = select(Product).where(Product.id == product_id)
            result = await session.execute(query)
            product = result.scalars().first()

        return product

    async def update_product_count(self, product_id: int, new_count) -> Product:
        async with async_session() as session:
            stmt = update(Product).where(Product.id == product_id).values(count=new_count)
            await session.execute(stmt)
            await session.commit()

            upd_product = await self.get_product_by_id(product_id)
            return upd_product

    async def create_product(self, new_product: ProductCreate, seller_inn: int) -> Product:
        product_dc = new_product.dict()
        product_dc["seller_inn"] = seller_inn
        product_dc["id"] = await self.generate_id()
        async with async_session() as session:
            stmt = insert(Product).values(**product_dc)
            await session.execute(stmt)
            await session.commit()

            new_product = await self.get_product_by_id(product_dc["id"])
            return new_product

    async def edit_product(self, edited_product: ProductEdit, product_id: int) -> Product:
        product_dc = edited_product.dict()
        async with async_session() as session:
            stmt = update(Product).where(Product.id == product_id).values(**product_dc)
            await session.execute(stmt)
            await session.commit()

            product = await self.get_product_by_id(product_id)
            return product

    async def delete_product_by_id(self, product_id: int) -> None:
        async with async_session() as session:
            stmt = delete(Product).where(Product.id == product_id)
            await session.execute(stmt)
            await session.commit()
