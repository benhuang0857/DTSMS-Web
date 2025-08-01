from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import func
from typing import Optional, List
from models import Recipe as RecipeModel
from models import RecipeStep as RecipeStepModel
from models import Library as LibraryModel
from models import Autoflow as AutoflowModel
from models import ProcessingStep as ProcessingStepModel
from schemas.recipe import Recipe, RecipeWithRelations, RecipeWithSteps, RecipeWithFull, RecipeCreate, RecipeUpdate
from database import get_db
from routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[RecipeWithFull])
def get_recipes(skip: int = 0, limit: int = 10, 
                db: Session = Depends(get_db), 
                current_user: dict = Depends(get_current_user)):
    """
    獲取配方列表（包含完整的關聯資料：recipe_steps、autoflows 和 processing_steps）
    """
    try:
        # 查詢配方
        recipes = db.query(RecipeModel).offset(skip).limit(limit).all()
        
        # 轉換為 RecipeWithFull 格式
        recipe_list = []
        for recipe in recipes:
            # 查詢配方步驟
            recipe_steps = db.query(RecipeStepModel).filter(
                RecipeStepModel.recipe_id == recipe.id
            ).order_by(RecipeStepModel.number).all()
            
            # 查詢 autoflows
            autoflows = db.query(AutoflowModel).filter(
                AutoflowModel.recipe_id == recipe.id
            ).all()
            
            # 準備 autoflows 資料（包含 processing_steps）
            autoflows_data = []
            for autoflow in autoflows:
                # 查詢該 autoflow 的 processing_steps
                processing_steps = db.query(ProcessingStepModel).filter(
                    ProcessingStepModel.autoflow_id == autoflow.id
                ).all()
                
                # 轉換 processing_steps 為字典格式
                processing_steps_data = [
                    {
                        "id": step.id,
                        "name": step.name,
                        "description": step.description,
                        "created_time": step.created_time,
                        "updated_time": step.updated_time
                    } for step in processing_steps
                ]
                
                autoflows_data.append({
                    "id": autoflow.id,
                    "name": autoflow.name,
                    "description": autoflow.description,
                    "status": autoflow.status,
                    "created_time": autoflow.created_time,
                    "updated_time": autoflow.updated_time,
                    "processing_steps": processing_steps_data
                })
            
            # 取得 library 名稱
            library_name = None
            if recipe.library_id:
                library = db.query(LibraryModel).filter(
                    LibraryModel.id == recipe.library_id
                ).first()
                if library:
                    library_name = library.name
            
            recipe_list.append(
                RecipeWithFull(
                    id=recipe.id,
                    library_id=recipe.library_id,
                    name=recipe.name,
                    description=recipe.description,
                    status=recipe.status,
                    allow_parallel_autoflows=recipe.allow_parallel_autoflows,
                    created_time=recipe.created_time,
                    updated_time=recipe.updated_time,
                    library_name=library_name,
                    recipe_steps_count=len(recipe_steps),
                    autoflows_count=len(autoflows_data),
                    recipe_steps=recipe_steps,
                    autoflows=autoflows_data
                )
            )
        
        return recipe_list
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫錯誤: {str(e)}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"伺服器內部錯誤: {str(e)}"}
        )

@router.get("/{recipe_id}", response_model=RecipeWithSteps)
def get_recipe(recipe_id: int, 
               db: Session = Depends(get_db),
               current_user: dict = Depends(get_current_user)):
    """
    根據 ID 獲取特定的配方（包含步驟）
    """
    try:
        # 查詢配方
        recipe = db.query(RecipeModel).filter(
            RecipeModel.id == recipe_id
        ).first()
        
        if not recipe:
            raise HTTPException(status_code=404, detail="配方未找到")
        
        # 查詢配方步驟
        recipe_steps = db.query(RecipeStepModel).filter(
            RecipeStepModel.recipe_id == recipe_id
        ).order_by(RecipeStepModel.number).all()
        
        # 取得 library 名稱
        library_name = None
        if recipe.library_id:
            library = db.query(LibraryModel).filter(
                LibraryModel.id == recipe.library_id
            ).first()
            if library:
                library_name = library.name
        
        # 計算 autoflows 數量
        autoflows_count = db.query(AutoflowModel).filter(
            AutoflowModel.recipe_id == recipe.id
        ).count()
        
        return RecipeWithSteps(
            id=recipe.id,
            library_id=recipe.library_id,
            name=recipe.name,
            description=recipe.description,
            status=recipe.status,
            allow_parallel_autoflows=recipe.allow_parallel_autoflows,
            created_time=recipe.created_time,
            updated_time=recipe.updated_time,
            library_name=library_name,
            recipe_steps_count=len(recipe_steps),
            autoflows_count=autoflows_count,
            recipe_steps=recipe_steps
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫錯誤: {str(e)}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"伺服器內部錯誤: {str(e)}"}
        )

@router.post("/", response_model=Recipe)
def create_recipe(recipe: RecipeCreate, 
                  db: Session = Depends(get_db),
                  current_user: dict = Depends(get_current_user)):
    """
    創建新的配方（包含步驟）
    """
    try:
        # 如果有 library_id，驗證 library 是否存在
        if recipe.library_id:
            library = db.query(LibraryModel).filter(
                LibraryModel.id == recipe.library_id
            ).first()
            
            if not library:
                raise HTTPException(status_code=404, detail="Library 未找到")
        
        # 創建配方
        db_recipe = RecipeModel(
            library_id=recipe.library_id,
            name=recipe.name,
            description=recipe.description,
            status=recipe.status,
            allow_parallel_autoflows=recipe.allow_parallel_autoflows
        )
        
        db.add(db_recipe)
        db.flush()  # 先 flush 以取得 recipe ID
        
        # 創建配方步驟
        if recipe.recipe_steps:
            for step_data in recipe.recipe_steps:
                db_step = RecipeStepModel(
                    recipe_id=db_recipe.id,
                    number=step_data.number,
                    action=step_data.action,
                    parameters=step_data.parameters,
                    status=step_data.status
                )
                db.add(db_step)
        
        db.commit()
        db.refresh(db_recipe)
        
        return db_recipe
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫完整性錯誤: {str(e)}"}
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫錯誤: {str(e)}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"伺服器內部錯誤: {str(e)}"}
        )

@router.put("/{recipe_id}", response_model=Recipe)
def update_recipe(recipe_id: int, 
                  recipe: RecipeUpdate,
                  db: Session = Depends(get_db),
                  current_user: dict = Depends(get_current_user)):
    """
    更新配方（包含步驟）
    """
    try:
        # 查詢配方
        db_recipe = db.query(RecipeModel).filter(
            RecipeModel.id == recipe_id
        ).first()
        
        if not db_recipe:
            raise HTTPException(status_code=404, detail="配方未找到")
        
        # 如果有 library_id，驗證 library 是否存在
        if recipe.library_id:
            library = db.query(LibraryModel).filter(
                LibraryModel.id == recipe.library_id
            ).first()
            
            if not library:
                raise HTTPException(status_code=404, detail="Library 未找到")
        
        # 更新欄位
        update_data = recipe.dict(exclude_unset=True)
        recipe_steps = update_data.pop('recipe_steps', None)
        
        for key, value in update_data.items():
            setattr(db_recipe, key, value)
        
        # 如果有提供 recipe_steps，則更新配方步驟
        if recipe_steps is not None:
            # 刪除現有的配方步驟
            db.query(RecipeStepModel).filter(
                RecipeStepModel.recipe_id == recipe_id
            ).delete()
            
            # 創建新的配方步驟
            for step_data in recipe_steps:
                db_step = RecipeStepModel(
                    recipe_id=db_recipe.id,
                    number=step_data.number,
                    action=step_data.action,
                    parameters=step_data.parameters,
                    status=step_data.status
                )
                db.add(db_step)
        
        db.commit()
        db.refresh(db_recipe)
        
        return db_recipe
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫完整性錯誤: {str(e)}"}
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫錯誤: {str(e)}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"伺服器內部錯誤: {str(e)}"}
        )

@router.delete("/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int,
                  db: Session = Depends(get_db),
                  current_user: dict = Depends(get_current_user)):
    """
    刪除配方（會自動刪除相關的步驟和 autoflows）
    """
    try:
        # 查詢配方
        db_recipe = db.query(RecipeModel).filter(
            RecipeModel.id == recipe_id
        ).first()
        
        if not db_recipe:
            raise HTTPException(status_code=404, detail="配方未找到")
        
        # 先刪除相關的 autoflows（會連帶刪除 processing_steps）
        autoflows = db.query(AutoflowModel).filter(
            AutoflowModel.recipe_id == recipe_id
        ).all()
        
        for autoflow in autoflows:
            db.delete(autoflow)
        
        # 刪除配方步驟（由於設置了 cascade，這可能不需要）
        db.query(RecipeStepModel).filter(
            RecipeStepModel.recipe_id == recipe_id
        ).delete()
        
        # 刪除配方
        db.delete(db_recipe)
        db.commit()
        
        return {"message": "配方已成功刪除"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫錯誤: {str(e)}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"伺服器內部錯誤: {str(e)}"}
        )

@router.get("/{recipe_id}/full", response_model=RecipeWithFull)
def get_recipe_full(recipe_id: int, 
                    db: Session = Depends(get_db),
                    current_user: dict = Depends(get_current_user)):
    """
    根據 ID 獲取完整的配方資訊（包含 recipe_steps、autoflows 和 processing_steps）
    """
    try:
        # 查詢配方
        recipe = db.query(RecipeModel).filter(
            RecipeModel.id == recipe_id
        ).first()
        
        if not recipe:
            raise HTTPException(status_code=404, detail="配方未找到")
        
        # 查詢配方步驟
        recipe_steps = db.query(RecipeStepModel).filter(
            RecipeStepModel.recipe_id == recipe_id
        ).order_by(RecipeStepModel.number).all()
        
        # 查詢 autoflows
        autoflows = db.query(AutoflowModel).filter(
            AutoflowModel.recipe_id == recipe_id
        ).all()
        
        # 準備 autoflows 資料（包含 processing_steps）
        autoflows_data = []
        for autoflow in autoflows:
            # 查詢該 autoflow 的 processing_steps
            processing_steps = db.query(ProcessingStepModel).filter(
                ProcessingStepModel.autoflow_id == autoflow.id
            ).all()
            
            # 轉換 processing_steps 為字典格式
            processing_steps_data = [
                {
                    "id": step.id,
                    "name": step.name,
                    "description": step.description,
                    "created_time": step.created_time,
                    "updated_time": step.updated_time
                } for step in processing_steps
            ]
            
            autoflows_data.append({
                "id": autoflow.id,
                "name": autoflow.name,
                "description": autoflow.description,
                "status": autoflow.status,
                "created_time": autoflow.created_time,
                "updated_time": autoflow.updated_time,
                "processing_steps": processing_steps_data
            })
        
        # 取得 library 名稱
        library_name = None
        if recipe.library_id:
            library = db.query(LibraryModel).filter(
                LibraryModel.id == recipe.library_id
            ).first()
            if library:
                library_name = library.name
        
        return RecipeWithFull(
            id=recipe.id,
            library_id=recipe.library_id,
            name=recipe.name,
            description=recipe.description,
            status=recipe.status,
            allow_parallel_autoflows=recipe.allow_parallel_autoflows,
            created_time=recipe.created_time,
            updated_time=recipe.updated_time,
            library_name=library_name,
            recipe_steps_count=len(recipe_steps),
            autoflows_count=len(autoflows_data),
            recipe_steps=recipe_steps,
            autoflows=autoflows_data
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫錯誤: {str(e)}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"伺服器內部錯誤: {str(e)}"}
        )