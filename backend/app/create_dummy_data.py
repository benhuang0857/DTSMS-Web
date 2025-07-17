#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
創建 Recipe、Autoflow、Processing Steps 的 dummy data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Recipe, RecipeStep, Autoflow, ProcessingStep, Library
from enums import BasicStatus
from datetime import datetime

def create_dummy_data():
    """創建測試資料"""
    db = SessionLocal()
    
    try:
        print("開始創建 dummy data...")
        
        # 檢查是否已有資料
        existing_recipes = db.query(Recipe).count()
        if existing_recipes > 0:
            print("已存在 {} 個 recipe，跳過創建...".format(existing_recipes))
            return
        
        # 1. 創建 Recipe 資料
        print("創建 Recipe 資料...")
        
        recipes_data = [
            {
                "name": "網站漏洞掃描配方",
                "description": "標準的網站安全漏洞掃描配方，包含多個掃描步驟",
                "status": BasicStatus.active,
                "library_id": None,
                "steps": [
                    {"number": 1, "action": "port_scan", "parameters": {"timeout": 30, "ports": "80,443,8080"}},
                    {"number": 2, "action": "vulnerability_scan", "parameters": {"deep_scan": True, "check_ssl": True}},
                    {"number": 3, "action": "directory_scan", "parameters": {"wordlist": "common.txt"}},
                    {"number": 4, "action": "sql_injection_test", "parameters": {"payloads": "basic"}},
                    {"number": 5, "action": "report_generation", "parameters": {"format": "pdf", "include_details": True}}
                ]
            },
            {
                "name": "API 安全測試配方",
                "description": "專門針對 API 端點的安全測試配方",
                "status": BasicStatus.active,
                "library_id": None,
                "steps": [
                    {"number": 1, "action": "api_discovery", "parameters": {"swagger_check": True}},
                    {"number": 2, "action": "authentication_test", "parameters": {"test_bypass": True}},
                    {"number": 3, "action": "authorization_test", "parameters": {"test_privilege_escalation": True}},
                    {"number": 4, "action": "input_validation_test", "parameters": {"test_injection": True}},
                    {"number": 5, "action": "rate_limiting_test", "parameters": {"max_requests": 1000}}
                ]
            },
            {
                "name": "行動應用程式掃描配方",
                "description": "行動應用程式（APK/IPA）的安全掃描配方",
                "status": BasicStatus.active,
                "library_id": None,
                "steps": [
                    {"number": 1, "action": "app_info_extraction", "parameters": {"extract_manifest": True}},
                    {"number": 2, "action": "static_analysis", "parameters": {"check_permissions": True}},
                    {"number": 3, "action": "dynamic_analysis", "parameters": {"runtime_check": True}},
                    {"number": 4, "action": "network_analysis", "parameters": {"intercept_traffic": True}},
                    {"number": 5, "action": "crypto_analysis", "parameters": {"check_encryption": True}}
                ]
            },
            {
                "name": "網路設備掃描配方",
                "description": "針對網路設備（路由器、交換機等）的掃描配方",
                "status": BasicStatus.active,
                "library_id": None,
                "steps": [
                    {"number": 1, "action": "device_discovery", "parameters": {"snmp_check": True}},
                    {"number": 2, "action": "service_enumeration", "parameters": {"check_telnet": True, "check_ssh": True}},
                    {"number": 3, "action": "default_credentials_test", "parameters": {"common_passwords": True}},
                    {"number": 4, "action": "firmware_analysis", "parameters": {"check_version": True}},
                    {"number": 5, "action": "configuration_audit", "parameters": {"security_baseline": True}}
                ]
            }
        ]
        
        created_recipes = []
        for recipe_data in recipes_data:
            # 創建 Recipe
            recipe = Recipe(
                name=recipe_data["name"],
                description=recipe_data["description"],
                status=recipe_data["status"],
                library_id=recipe_data["library_id"]
            )
            db.add(recipe)
            db.flush()  # 取得 ID
            
            # 創建 Recipe Steps
            for step_data in recipe_data["steps"]:
                recipe_step = RecipeStep(
                    recipe_id=recipe.id,
                    number=step_data["number"],
                    action=step_data["action"],
                    parameters=step_data["parameters"],
                    status=BasicStatus.active
                )
                db.add(recipe_step)
            
            created_recipes.append(recipe)
            print("  - 創建 Recipe: {}".format(recipe.name))
        
        db.commit()
        print("成功創建 {} 個 Recipe".format(len(created_recipes)))
        
        # 2. 創建 Autoflow 資料
        print("創建 Autoflow 資料...")
        
        autoflows_data = [
            {
                "recipe_id": created_recipes[0].id,  # 網站漏洞掃描配方
                "name": "生產環境網站掃描流程",
                "description": "針對生產環境的網站進行全面的安全掃描",
                "status": BasicStatus.active,
                "steps": [
                    {"name": "Step 1: 初始連接檢測", "description": "檢查目標網站的連接狀態和基本資訊"},
                    {"name": "Step 2: 漏洞掃描", "description": "執行全面的漏洞掃描"},
                    {"name": "Step 3: 深度分析", "description": "對發現的漏洞進行深度分析"},
                    {"name": "Step 4: 風險評估", "description": "評估漏洞的風險等級和影響範圍"},
                    {"name": "Step 5: 報告生成", "description": "生成詳細的掃描報告"}
                ]
            },
            {
                "recipe_id": created_recipes[0].id,  # 網站漏洞掃描配方
                "name": "測試環境網站掃描流程",
                "description": "針對測試環境的網站進行快速掃描",
                "status": BasicStatus.active,
                "steps": [
                    {"name": "Step 1: 快速掃描", "description": "執行快速的基礎掃描"},
                    {"name": "Step 2: 基本檢測", "description": "檢測常見的安全問題"},
                    {"name": "Step 3: 簡易報告", "description": "生成簡化的掃描報告"}
                ]
            },
            {
                "recipe_id": created_recipes[1].id,  # API 安全測試配方
                "name": "API 安全測試流程",
                "description": "對 API 端點進行全面的安全測試",
                "status": BasicStatus.active,
                "steps": [
                    {"name": "Step 1: API 發現", "description": "自動發現 API 端點"},
                    {"name": "Step 2: 認證測試", "description": "測試 API 認證機制"},
                    {"name": "Step 3: 授權測試", "description": "測試 API 授權控制"},
                    {"name": "Step 4: 輸入驗證測試", "description": "測試 API 輸入驗證"},
                    {"name": "Step 5: 效能測試", "description": "測試 API 效能和限流"}
                ]
            },
            {
                "recipe_id": created_recipes[2].id,  # 行動應用程式掃描配方
                "name": "Android 應用程式掃描流程",
                "description": "針對 Android 應用程式的全面安全掃描",
                "status": BasicStatus.active,
                "steps": [
                    {"name": "Step 1: APK 解析", "description": "解析 APK 檔案結構"},
                    {"name": "Step 2: 靜態分析", "description": "進行程式碼靜態分析"},
                    {"name": "Step 3: 動態分析", "description": "執行動態行為分析"},
                    {"name": "Step 4: 網路分析", "description": "分析網路通訊行為"},
                    {"name": "Step 5: 安全報告", "description": "生成安全評估報告"}
                ]
            },
            {
                "recipe_id": created_recipes[2].id,  # 行動應用程式掃描配方
                "name": "iOS 應用程式掃描流程",
                "description": "針對 iOS 應用程式的全面安全掃描",
                "status": BasicStatus.active,
                "steps": [
                    {"name": "Step 1: IPA 解析", "description": "解析 IPA 檔案結構"},
                    {"name": "Step 2: 靜態分析", "description": "進行程式碼靜態分析"},
                    {"name": "Step 3: 動態分析", "description": "執行動態行為分析"},
                    {"name": "Step 4: 隱私檢測", "description": "檢測隱私權限使用"},
                    {"name": "Step 5: 安全報告", "description": "生成安全評估報告"}
                ]
            },
            {
                "recipe_id": created_recipes[3].id,  # 網路設備掃描配方
                "name": "企業網路設備掃描流程",
                "description": "針對企業網路設備的全面安全掃描",
                "status": BasicStatus.active,
                "steps": [
                    {"name": "Step 1: 設備發現", "description": "自動發現網路中的設備"},
                    {"name": "Step 2: 服務枚舉", "description": "枚舉設備開放的服務"},
                    {"name": "Step 3: 弱點檢測", "description": "檢測設備的安全弱點"},
                    {"name": "Step 4: 配置審計", "description": "審計設備安全配置"},
                    {"name": "Step 5: 合規檢查", "description": "檢查是否符合安全標準"}
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
                status=autoflow_data["status"]
            )
            db.add(autoflow)
            db.flush()  # 取得 ID
            
            # 創建 Processing Steps
            for step_data in autoflow_data["steps"]:
                processing_step = ProcessingStep(
                    autoflow_id=autoflow.id,
                    name=step_data["name"],
                    description=step_data["description"]
                )
                db.add(processing_step)
            
            created_autoflows.append(autoflow)
            print("  - 創建 Autoflow: {}".format(autoflow.name))
        
        db.commit()
        print("成功創建 {} 個 Autoflow".format(len(created_autoflows)))
        
        # 統計資訊
        total_recipe_steps = db.query(RecipeStep).count()
        total_processing_steps = db.query(ProcessingStep).count()
        
        print("\n=== 創建完成 ===")
        print("Recipes: {}".format(len(created_recipes)))
        print("Recipe Steps: {}".format(total_recipe_steps))
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