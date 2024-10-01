from decimal import Decimal, ROUND_HALF_UP
import math
import pandas as pd

class Calculator:
    @staticmethod
    def calculate_ideal_size(days, last_sales_day, tvu, remove_product):
        if days is None or last_sales_day is None:
            return '0'

        if any(val in ['PRODUCTO SIN CARGA', 'PRODUCTO SIN VENTA'] for val in [days, last_sales_day, tvu, remove_product]):
            return '0'

        if days == 0:
            return '0'

        return str(math.trunc((last_sales_day / days) * (tvu - remove_product)))

    @staticmethod
    def evaluate_masterpack(ddi_master_pack, tvu, stock, last_sales_day):
        if ddi_master_pack in ['PRODUCTO SIN VENTA', 'PRODUCTO SIN CARGA']:
            return ddi_master_pack.upper()

        if pd.isna(ddi_master_pack):
            return 'PRODUCTO SIN CARGA'

        try:
            ddi_master_pack = float(ddi_master_pack)
        except ValueError:
            return 'PRODUCTO SIN CARGA'

        if ddi_master_pack <= tvu:
            return 'OK'
        elif stock == 0 and last_sales_day == 0:
            return 'PRODUCTO SIN CARGA'
        elif stock > 0 and last_sales_day == 0:
            return 'PRODUCTO SIN VENTA'
        else:
            return 'BAJAR MASTERPACK'

    @staticmethod
    def evaluate_packqty(ddi_packqty, tvu, stock, last_sales_day):
        if ddi_packqty in ['PRODUCTO SIN VENTA', 'PRODUCTO SIN CARGA']:
            return ddi_packqty.upper()

        if pd.isna(ddi_packqty):
            return 'PRODUCTO SIN CARGA'

        try:
            ddi_packqty = float(ddi_packqty)
        except ValueError:
            return 'PRODUCTO SIN CARGA'

        if ddi_packqty <= tvu:
            return 'OK'
        elif stock == 0 and last_sales_day == 0:
            return 'PRODUCTO SIN CARGA'
        elif stock > 0 and last_sales_day == 0:
            return 'PRODUCTO SIN VENTA'
        else:
            return 'BAJAR PACKQTY'

    @staticmethod
    def evaluate_innerpack(ddi_innerpack, tvu, stock, last_sales_day):
        if ddi_innerpack in ['PRODUCTO SIN VENTA', 'PRODUCTO SIN CARGA']:
            return ddi_innerpack.upper()

        if pd.isna(ddi_innerpack):
            return 'PRODUCTO SIN CARGA'

        try:
            ddi_innerpack = float(ddi_innerpack)
        except ValueError:
            return 'PRODUCTO SIN CARGA'

        if ddi_innerpack <= tvu:
            return 'OK'
        elif stock == 0 and last_sales_day == 0:
            return 'PRODUCTO SIN CARGA'
        elif stock > 0 and last_sales_day == 0:
            return 'PRODUCTO SIN VENTA'
        else:
            return 'BAJAR INNERPACK'

    @staticmethod
    def safe_round(value):
        try:
            value_data = Decimal(str(value))
            return value_data.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        except:
            return value