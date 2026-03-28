from flask import Blueprint, jsonify
from src.config.database import DatabaseConfig
from sqlalchemy import text

membresia_bp = Blueprint('membresias', __name__, url_prefix='/api/membresias')

@membresia_bp.route('', methods=['GET'])
def listar_membresias():
    """GET /api/membresias - Listar todos los planes"""
    db_config = DatabaseConfig()
    engine = db_config.create_engine()
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, tipo, precio, descripcion, duracion_dias FROM membresias"))
        membresias = []
        for row in result:
            membresias.append({
                'id': row[0],
                'tipo': row[1],
                'precio': float(row[2]),
                'descripcion': row[3],
                'duracion_dias': row[4]
            })
    
    return jsonify(membresias)