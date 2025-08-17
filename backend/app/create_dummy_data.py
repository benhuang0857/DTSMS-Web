#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
創建 Library、LibraryAction、Recipe、Autoflow、Processing Steps 的 dummy data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Recipe, RecipeStep, Autoflow, ProcessingStep, Library, LibraryAction
from enums import BasicStatus
from datetime import datetime

def create_dummy_data():
    """創建測試資料"""
    db = SessionLocal()
    
    try:
        print("開始創建 dummy data...")
        
        # 檢查是否已有資料
        existing_libraries = db.query(Library).count()
        if existing_libraries > 0:
            print("已存在 {} 個 library，跳過創建...".format(existing_libraries))
            return
        
        # 1. 首先創建 Libraries
        print("創建 Library 資料...")
        
        libraries_data = [
            {
                "name": "OpSWAT Core",
                "api_endpoint": "https://api.opswat.com/v4",
                "docker_image": "opswat/core:latest",
                "api_key": "demo_key_12345",
                "description": "OpSWAT 核心惡意軟體掃描引擎",
                "status": BasicStatus.active
            },
            {
                "name": "Nmap Scanner",
                "api_endpoint": "http://nmap-service:8080/api/v1",
                "docker_image": "instrumentisto/nmap:latest",
                "description": "網路探索和安全掃描工具",
                "status": BasicStatus.active
            },
            {
                "name": "OWASP ZAP",
                "api_endpoint": "http://zap-service:8090/JSON",
                "docker_image": "owasp/zap2docker-stable:latest",
                "description": "網路應用程式安全掃描工具",
                "status": BasicStatus.active
            },
            {
                "name": "VirusTotal",
                "api_endpoint": "https://www.virustotal.com/vtapi/v2",
                "api_key": "your_virustotal_api_key",
                "description": "線上檔案和 URL 掃描服務",
                "status": BasicStatus.active
            }
        ]
        
        created_libraries = []
        for lib_data in libraries_data:
            library = Library(
                name=lib_data["name"],
                api_endpoint=lib_data["api_endpoint"],
                docker_image=lib_data.get("docker_image"),
                api_key=lib_data.get("api_key"),
                description=lib_data["description"],
                status=lib_data["status"]
            )
            db.add(library)
            db.flush()
            created_libraries.append(library)
            print("  - 創建 Library: {}".format(library.name))
        
        # 2. 創建 Library Actions
        print("創建 Library Actions...")
        
        actions_data = [
            # OpSWAT Core Actions
            {
                "library_id": created_libraries[0].id,
                "name": "檔案掃描",
                "api_path": "/file/scan",
                "http_method": "POST",
                "description": "上傳檔案進行惡意軟體掃描",
                "execution_order": 1
            },
            {
                "library_id": created_libraries[0].id,
                "name": "雜湊查詢",
                "api_path": "/file/hash",
                "http_method": "GET",
                "description": "根據檔案雜湊查詢掃描結果",
                "execution_order": 2
            },
            # Nmap Actions
            {
                "library_id": created_libraries[1].id,
                "name": "主機發現",
                "api_path": "/scan/discovery",
                "http_method": "POST",
                "description": "發現網路中的活躍主機",
                "execution_order": 1
            },
            {
                "library_id": created_libraries[1].id,
                "name": "端口掃描",
                "api_path": "/scan/ports",
                "http_method": "POST",
                "description": "掃描目標主機的開放端口",
                "execution_order": 2
            },
            {
                "library_id": created_libraries[1].id,
                "name": "服務辨識",
                "api_path": "/scan/services",
                "http_method": "POST",
                "description": "辨識開放端口上的服務版本",
                "execution_order": 3
            },
            # OWASP ZAP Actions
            {
                "library_id": created_libraries[2].id,
                "name": "被動掃描",
                "api_path": "/pscan/action/scan",
                "http_method": "GET",
                "description": "被動式網路應用程式掃描",
                "execution_order": 1
            },
            {
                "library_id": created_libraries[2].id,
                "name": "主動掃描",
                "api_path": "/ascan/action/scan",
                "http_method": "GET",
                "description": "主動式網路應用程式掃描",
                "execution_order": 2
            },
            {
                "library_id": created_libraries[2].id,
                "name": "產生報告",
                "api_path": "/core/action/htmlreport",
                "http_method": "GET",
                "description": "產生 HTML 格式掃描報告",
                "execution_order": 3
            },
            # VirusTotal Actions
            {
                "library_id": created_libraries[3].id,
                "name": "檔案上傳掃描",
                "api_path": "/file/scan",
                "http_method": "POST",
                "description": "上傳檔案到 VirusTotal 進行掃描",
                "execution_order": 1
            },
            {
                "library_id": created_libraries[3].id,
                "name": "檔案報告查詢",
                "api_path": "/file/report",
                "http_method": "POST",
                "description": "查詢檔案掃描報告",
                "execution_order": 2
            }
        ]
        
        created_actions = []
        for action_data in actions_data:
            action = LibraryAction(
                library_id=action_data["library_id"],
                name=action_data["name"],
                api_path=action_data["api_path"],
                http_method=action_data["http_method"],
                description=action_data["description"],
                execution_order=action_data["execution_order"],
                status=BasicStatus.active
            )
            db.add(action)
            db.flush()
            created_actions.append(action)
            # 找到對應的 library
            library_name = next((lib.name for lib in created_libraries if lib.id == action_data["library_id"]), "Unknown")
            print("  - 創建 Action: {} ({})".format(action.name, library_name))
        
        # 3. 創建 Recipe 資料 (移除 library_id)
        print("創建 Recipe 資料...")
        
        recipes_data = [
            {
                "name": "惡意軟體分析配方",
                "description": "全面的惡意軟體檔案分析流程",
                "status": BasicStatus.active,
                "allow_parallel_autoflows": False
            },
            {
                "name": "網路安全掃描配方", 
                "description": "網路基礎設施安全掃描流程",
                "status": BasicStatus.active,
                "allow_parallel_autoflows": True
            },
            {
                "name": "網站應用程式測試配方",
                "description": "網站應用程式安全測試流程",
                "status": BasicStatus.active,
                "allow_parallel_autoflows": False
            }
        ]
        
        created_recipes = []
        for recipe_data in recipes_data:
            # 創建 Recipe (移除 library_id)
            recipe = Recipe(
                name=recipe_data["name"],
                description=recipe_data["description"],
                status=recipe_data["status"],
                allow_parallel_autoflows=recipe_data["allow_parallel_autoflows"]
            )
            db.add(recipe)
            db.flush()  # 取得 ID
            created_recipes.append(recipe)
            print("  - 創建 Recipe: {}".format(recipe.name))
        
        # 4. 創建 Autoflow 資料
        print("創建 Autoflow 資料...")
        
        autoflows_data = [
            {
                "recipe_id": created_recipes[0].id,  # 惡意軟體分析配方
                "name": "檔案惡意軟體分析流程",
                "description": "使用多個引擎分析檔案的惡意軟體",
                "status": BasicStatus.active,
                "allow_parallel_steps": False,
                "execution_order": 1,
                "steps": [
                    {"name": "OpSWAT 檔案掃描", "description": "使用 OpSWAT 引擎掃描檔案", "execution_order": 1, "library_action_id": created_actions[0].id},
                    {"name": "VirusTotal 檔案掃描", "description": "上傳到 VirusTotal 進行掃描", "execution_order": 2, "library_action_id": created_actions[8].id},
                    {"name": "VirusTotal 報告查詢", "description": "查詢 VirusTotal 掃描報告", "execution_order": 3, "library_action_id": created_actions[9].id}
                ]
            },
            {
                "recipe_id": created_recipes[1].id,  # 網路安全掃描配方
                "name": "網路基礎設施掃描流程",
                "description": "全面掃描網路基礎設施安全狀況",
                "status": BasicStatus.active,
                "allow_parallel_steps": True,
                "execution_order": 1,
                "steps": [
                    {"name": "主機發現", "description": "發現網路中的活躍主機", "execution_order": 1, "library_action_id": created_actions[2].id},
                    {"name": "端口掃描", "description": "掃描目標主機的開放端口", "execution_order": 2, "library_action_id": created_actions[3].id},
                    {"name": "服務辨識", "description": "辨識開放端口上的服務版本", "execution_order": 3, "library_action_id": created_actions[4].id}
                ]
            },
            {
                "recipe_id": created_recipes[2].id,  # 網站應用程式測試配方
                "name": "網站安全掃描流程",
                "description": "使用 OWASP ZAP 進行網站安全測試",
                "status": BasicStatus.active,
                "allow_parallel_steps": False,
                "execution_order": 1,
                "steps": [
                    {"name": "被動掃描", "description": "進行被動式安全掃描", "execution_order": 1, "library_action_id": created_actions[5].id},
                    {"name": "主動掃描", "description": "進行主動式安全掃描", "execution_order": 2, "library_action_id": created_actions[6].id},
                    {"name": "產生報告", "description": "產生詳細掃描報告", "execution_order": 3, "library_action_id": created_actions[7].id}
                ]
            }
        ]
        
        created_autoflows = []
        for autoflow_data in autoflows_data:
            # 創建 Autoflow
            autoflow = Autoflow(
                recipe_id=autoflow_data["recipe_id"],
                name=autoflow_data["name"],
                description=autoflow_data["description"],
                status=autoflow_data["status"],
                allow_parallel_steps=autoflow_data["allow_parallel_steps"],
                execution_order=autoflow_data["execution_order"]
            )
            db.add(autoflow)
            db.flush()  # 取得 ID
            
            # 創建 Processing Steps (新增 library_action_id)
            for step_data in autoflow_data["steps"]:
                processing_step = ProcessingStep(
                    autoflow_id=autoflow.id,
                    library_action_id=step_data["library_action_id"],
                    name=step_data["name"],
                    description=step_data["description"],
                    execution_order=step_data["execution_order"]
                )
                db.add(processing_step)
            
            created_autoflows.append(autoflow)
            print("  - 創建 Autoflow: {}".format(autoflow.name))
        
        db.commit()
        print("成功創建 {} 個 Autoflow".format(len(created_autoflows)))
        
        # 統計資訊
        total_processing_steps = db.query(ProcessingStep).count()
        
        print("\n=== 創建完成 ===")
        print("Libraries: {}".format(len(created_libraries)))
        print("Library Actions: {}".format(len(created_actions)))
        print("Recipes: {}".format(len(created_recipes)))
        print("Autoflows: {}".format(len(created_autoflows)))
        print("Processing Steps: {}".format(total_processing_steps))
        
    except Exception as e:
        print("錯誤: {}".format(e))
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_dummy_data()