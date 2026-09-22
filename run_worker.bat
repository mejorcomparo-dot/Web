@echo off
setlocal
chcp 65001 >nul
title Grok Bot Worker - fefe5f32-8832-4b3d-8082-38d1628347cb
"C:\Users\Manuel Adrián\Desktop\Proyectos antigravity\miscelanea\.venv\Scripts\python.exe" "C:\Users\Manuel Adrián\Desktop\Proyectos antigravity\GROK\bridge_worker.py" %*
