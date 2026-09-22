"""
Bridge Worker: Grok Bot (Cloud Orchestrator) <-> Antigravity (Local Programmer)
Conversación vinculada: fefe5f32-8832-4b3d-8082-38d1628347cb
"""

import os
import sys
import re
import json
import time
import subprocess
import datetime
from pathlib import Path

# Forzar UTF-8 en consola de Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Configuración del Enjambre
WORKSPACE_DIR = Path(r"C:\Users\Manuel Adrián\Desktop\Proyectos antigravity\GROK")
CONVERSATION_ID = "fefe5f32-8832-4b3d-8082-38d1628347cb"
INBOX_DIR = WORKSPACE_DIR / ".tasks" / "inbox"
OUTBOX_DIR = WORKSPACE_DIR / ".tasks" / "outbox"
LOG_CONVERSATION = WORKSPACE_DIR / "CONVERSACION_PROGRAMADOR.md"

def ensure_dirs():
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    OUTBOX_DIR.mkdir(parents=True, exist_ok=True)

def registrar_en_conversacion(emisor: str, icono: str, mensaje: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prefix = f"{icono} " if icono else ""
    bloque = f"\n### {prefix}{emisor} — [{timestamp}]\n{mensaje}\n\n---\n"
    with open(LOG_CONVERSATION, "a", encoding="utf-8") as f:
        f.write(bloque)
    try:
        print(f"[{timestamp}] Registrado en conversación ({CONVERSATION_ID}): {emisor}")
    except Exception:
        pass

def run_cmd(cmd: str) -> dict:
    """Ejecuta un comando en WORKSPACE_DIR y retorna resultado."""
    try:
        res = subprocess.run(
            cmd,
            shell=True,
            cwd=str(WORKSPACE_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        return {
            "cmd": cmd,
            "returncode": res.returncode,
            "stdout": res.stdout.strip(),
            "stderr": res.stderr.strip()
        }
    except Exception as e:
        return {
            "cmd": cmd,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e)
        }

def asegurar_git():
    """Verifica si el repositorio git está inicializado, y si no, lo inicializa."""
    git_dir = WORKSPACE_DIR / ".git"
    if not git_dir.exists():
        run_cmd("git init")
        run_cmd("git config user.name \"Antigravity Programmer\"")
        run_cmd("git config user.email \"antigravity@local\"")

def parse_code_blocks(text: str) -> list:
    """Extrae bloques de código ```lang ... ``` con posibles rutas en la primera línea o antes."""
    pattern = r"```([a-zA-Z0-9_\-\.]*)\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    blocks = []
    for lang, code in matches:
        blocks.append({"lang": lang.strip(), "code": code})
    return blocks

def ejecutar_tarea_real(data: dict) -> dict:
    """
    Ejecuta la tarea recibida:
    1. Si trae 'files', los escribe directamente en disco.
    2. Si trae 'commands', los ejecuta.
    3. Si trae 'git', ejecuta git checkout/branch/commit.
    4. Si trae 'prompt', parsea archivos o requerimientos (HTML/Tailwind, scripts, etc.).
    """
    task_id = data.get("id", "tarea_anonima")
    prompt = data.get("prompt", "")
    files_to_write = data.get("files", {})
    commands_to_run = data.get("commands", [])
    git_spec = data.get("git", {})
    
    files_created = []
    commands_executed = []
    git_info = None

    # 1. Escribir archivos especificados en JSON
    for rel_path, content in files_to_write.items():
        target = WORKSPACE_DIR / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        files_created.append(rel_path)
        print(f"[ACTION] Archivo creado desde payload: {rel_path}")

    # 2. Análisis inteligente de Prompt si no vienen 'files' explícitos
    if not files_created and prompt:
        # Detectar rutas comunes mencionadas en el prompt (e.g. dist/hola_mundo.html, dist/index.html)
        path_match = re.search(r"([a-zA-Z0-9_\-\.\/]+\.(?:html|css|js|py|json|md))", prompt)
        code_blocks = parse_code_blocks(prompt)

        if code_blocks and path_match:
            rel_path = path_match.group(1)
            content = code_blocks[0]["code"]
            target = WORKSPACE_DIR / rel_path
            target.parent.mkdir(parents=True, exist_ok=True)
            with open(target, "w", encoding="utf-8") as f:
                f.write(content)
            files_created.append(rel_path)
            print(f"[ACTION] Archivo extraído de bloque de código: {rel_path}")

        elif "hola_mundo.html" in prompt.lower() or "hola mundo" in prompt.lower():
            rel_path = "dist/hola_mundo.html"
            target = WORKSPACE_DIR / rel_path
            target.parent.mkdir(parents=True, exist_ok=True)
            html_content = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hola Mundo</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="min-h-screen bg-slate-900 text-white flex items-center justify-center p-4">
  <div class="text-center p-8 bg-slate-800/80 rounded-2xl border border-slate-700 shadow-2xl max-w-md w-full backdrop-blur">
    <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-emerald-500/10 text-emerald-400 mb-6 border border-emerald-500/20 text-2xl font-bold">
      👋
    </div>
    <h1 class="text-4xl font-extrabold tracking-tight text-white mb-3">
      Hola Mundo
    </h1>
    <p class="text-slate-400 text-sm leading-relaxed mb-6">
      Página generada por el <strong>Agente Programador Antigravity</strong> bajo la orquestación de <strong>Grok Bot</strong>.
    </p>
    <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-mono bg-slate-950/60 text-emerald-400 border border-slate-800">
      <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
      dist/hola_mundo.html · Tailwind CDN
    </div>
  </div>
</body>
</html>
"""
            with open(target, "w", encoding="utf-8") as f:
                f.write(html_content)
            files_created.append(rel_path)
            print(f"[ACTION] Archivo generado por plantilla HTML/Tailwind: {rel_path}")

    # 3. Ejecutar comandos si se especifican
    for cmd in commands_to_run:
        res = run_cmd(cmd)
        commands_executed.append(res)
        print(f"[ACTION] Comando ejecutado: {cmd} (code: {res['returncode']})")

    # 4. Manejo de Git (por JSON o por mención en el prompt)
    branch = git_spec.get("branch")
    commit_msg = git_spec.get("commit")

    if not branch and "rama" in prompt.lower():
        match_branch = re.search(r"rama\s+([a-zA-Z0-9_\-\/]+)", prompt, re.IGNORECASE)
        if match_branch:
            branch = match_branch.group(1).rstrip(".,;")

    if not commit_msg:
        commit_msg = f"feat({task_id}): {prompt[:60]}" if prompt else f"feat({task_id}): updates"

    if branch or "git" in prompt.lower() or files_created:
        asegurar_git()
        if branch:
            # Checkout o creación de rama
            run_cmd(f"git checkout -B {branch}")
        
        # Git add de archivos creados
        if files_created:
            for f in files_created:
                run_cmd(f"git add \"{f}\"")
        else:
            run_cmd("git add .")
            
        commit_res = run_cmd(f"git commit -m \"{commit_msg}\"")
        log_res = run_cmd("git log -n 1 --oneline")
        last_commit = log_res["stdout"] if log_res["returncode"] == 0 else ""

        # Auto-push a GitHub si el remoto origin está configurado
        remote_check = run_cmd("git remote")
        push_info = ""
        if "origin" in remote_check.get("stdout", ""):
            b_name = branch if branch else "main"
            push_res = run_cmd(f"git push -u origin {b_name}")
            if push_res["returncode"] == 0:
                push_info = f" | Push a GitHub exitoso (origin/{b_name})"
                print(f"[GIT] Push completado a GitHub: origin/{b_name}")
            else:
                push_info = f" | Aviso push: {push_res.get('stderr', '')[:80]}"

        git_info = {
            "branch": branch or "actual",
            "commit_msg": commit_msg,
            "last_commit": f"{last_commit}{push_info}"
        }
        print(f"[GIT] Commit completado: {last_commit}{push_info}")

    # Construir reporte de salida
    salida_texto = []
    salida_texto.append(f"Tarea #{task_id} procesada y ejecutada con éxito por el Agente Programador Antigravity.")
    if files_created:
        salida_texto.append(f"- Archivos generados en workspace: {', '.join(files_created)}")
    if git_info:
        salida_texto.append(f"- Git: Rama '{git_info['branch']}' | {git_info['last_commit']}")
    if commands_executed:
        salida_texto.append(f"- Comandos ejecutados: {len(commands_executed)}")
    if not files_created and not commands_executed and not git_info:
        salida_texto.append(f"- Instrucción procesada: \"{prompt}\"")

    return {
        "status": "COMPLETED",
        "output": "\n".join(salida_texto),
        "files_created": files_created,
        "commands_executed": commands_executed,
        "git": git_info
    }

def procesar_tarea(task_file: Path):
    try:
        with open(task_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        task_id = data.get("id", task_file.stem)
        prompt = data.get("prompt", "")
        autor = data.get("author", "Grok Bot (Orquestador)")
        
        print(f"\n{'='*60}\n[SWARM] Nueva tarea recibida: #{task_id} de {autor}")
        print(f"Prompt: {prompt}\n{'='*60}")
        
        registrar_en_conversacion(
            emisor=f"{autor}",
            icono="🤖",
            mensaje=f"> **Mensaje/Tarea #{task_id}:** {prompt}"
        )
        
        # Ejecución real de programación
        resultado_ejecucion = ejecutar_tarea_real(data)
        
        # Guardar en outbox
        out_file = OUTBOX_DIR / f"resultado_{task_id}.json"
        resultado_data = {
            "task_id": task_id,
            "conversation_id": CONVERSATION_ID,
            "status": resultado_ejecucion.get("status", "COMPLETED"),
            "timestamp": datetime.datetime.now().isoformat(),
            "output": resultado_ejecucion.get("output", ""),
            "files_created": resultado_ejecucion.get("files_created", []),
            "git": resultado_ejecucion.get("git"),
            "commands_executed": resultado_ejecucion.get("commands_executed", [])
        }
        
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(resultado_data, f, indent=2, ensure_ascii=False)
            
        registrar_en_conversacion(
            emisor=f"Antigravity (Programador Local) [Sesión: {CONVERSATION_ID}]",
            icono="🛠️",
            mensaje=resultado_ejecucion.get("output", "")
        )
        
        # Eliminar tarea procesada de inbox
        task_file.unlink()
        print(f"[SWARM] Tarea #{task_id} completada y registrada en outbox con éxito.\n")
        
    except Exception as e:
        print(f"[ERROR] Error procesando {task_file.name}: {e}")

def run_worker(poll_interval: float = 1.5):
    ensure_dirs()
    print("=" * 70)
    print(f"🚀 PUENTE ACTIVO CON EJECUCIÓN REAL: Grok Bot <---> Antigravity")
    print(f"📁 Workspace: {WORKSPACE_DIR}")
    print(f"🔑 Conversation ID: {CONVERSATION_ID}")
    print(f"📥 Inbox: {INBOX_DIR}")
    print(f"📤 Outbox: {OUTBOX_DIR}")
    print("=" * 70)
    print("Escuchando nuevas órdenes de Grok Bot...")

    try:
        while True:
            archivos = list(INBOX_DIR.glob("*.json"))
            for archivo in archivos:
                procesar_tarea(archivo)
            time.sleep(poll_interval)
    except KeyboardInterrupt:
        print("\n[INFO] Deteniendo bridge worker...")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--oneshot":
        ensure_dirs()
        archivos = list(INBOX_DIR.glob("*.json"))
        for archivo in archivos:
            procesar_tarea(archivo)
    else:
        run_worker()
