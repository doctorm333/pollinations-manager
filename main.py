import customtkinter as ctk
import tkinter as tk
import json
import os
import sys
import subprocess
import requests
import webbrowser
import threading
import random
import base64
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import filedialog, messagebox
from io import BytesIO


# Free image hosting - no API keys required
def upload_image_to_hosting(image_path):
    """Upload image to free hosting and return URL"""

    # Try multiple services in order
    services = [
        upload_to_0x0,      # 0x0.st - simple, reliable
        upload_to_catbox,   # catbox.moe - popular
        upload_to_uguu,     # uguu.se - temporary
    ]

    for service in services:
        try:
            url = service(image_path)
            if url and url.startswith("http"):
                print(f"Upload success: {url}")
                return url
        except Exception as e:
            print(f"Service failed: {e}")
            continue

    return None


def upload_to_0x0(image_path):
    """Upload to 0x0.st - free, no registration"""
    with open(image_path, "rb") as f:
        response = requests.post(
            "https://0x0.st",
            files={"file": f},
            timeout=60
        )
        if response.status_code == 200:
            return response.text.strip()
    return None


def upload_to_catbox(image_path):
    """Upload to catbox.moe - free, permanent"""
    with open(image_path, "rb") as f:
        response = requests.post(
            "https://catbox.moe/user/api.php",
            files={"fileToUpload": f},
            data={"reqtype": "fileupload"},
            timeout=60
        )
        if response.status_code == 200:
            url = response.text.strip()
            if url.startswith("http"):
                return url
    return None


def upload_to_uguu(image_path):
    """Upload to uguu.se - temporary (48 hours)"""
    with open(image_path, "rb") as f:
        response = requests.post(
            "https://uguu.se/upload.php",
            files={"files[]": f},
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("files"):
                return data["files"][0]["url"]
    return None


def open_file_or_folder(path):
    """Cross-platform function to open file or folder"""
    if sys.platform == 'win32':
        os.startfile(path)
    elif sys.platform == 'darwin':  # macOS
        subprocess.run(['open', path])
    else:  # Linux
        subprocess.run(['xdg-open', path])

# --- LOCALIZATION ---

TRANSLATIONS = {
    "en": {
        # App
        "app_title": "Pollinations Manager | AI Chat Hub Edition",
        "version": "v2.0",

        # Sidebar
        "your_balance": "YOUR BALANCE",
        "pollen": "Pollen",
        "refresh": "Refresh",
        "save_folder": "Save Folder",
        "open_folder": "Open Folder",
        "theme": "Theme:",
        "language": "Language:",
        "our_telegram": "Our Telegram",

        # Tabs
        "tab_chat": "Chat",
        "tab_images": "Images",
        "tab_video": "Video",

        # Chat
        "model": "Model:",
        "save_chat": "Save",
        "clear_chat": "Clear",
        "send": "Send",
        "send_hint": "Ctrl+Enter to send",
        "chat_welcome": "Hello! I'm ready to help. Select a model and write your question.",
        "chat_cleared": "Chat cleared. Start a new conversation.",
        "you": "You",
        "ai": "AI",
        "copied": "Copied!",
        "nothing_to_save": "Nothing to save",
        "saved": "Saved",
        "generating_response": "Generating response...",

        # Generation
        "prompt_label": "Your prompt:",
        "generate": "GENERATE",
        "generating": "Generating... Please wait.",
        "size_format": "Size and Format:",
        "style": "Style:",
        "no_style": "No style",
        "duration_sec": "Duration (sec):",
        "generate_audio": "Generate audio (veo)",
        "high_quality": "High Quality / 4K",
        "reference_image": "Reference Image:",
        "select_image": "Select Image",
        "clear_image": "Clear",
        "no_image": "No image selected",
        "uploading_image": "Uploading image...",
        "upload_error": "Upload error",
        "image_ready_to_use": "Image ready",
        "supported_models": "Supported: kontext, seedance, wan",

        # Status
        "ready": "Ready",
        "api_online": "API Online",
        "generating_image": "Generating image...",
        "generating_video": "Generating video...",
        "generating_text": "Generating text...",
        "image_ready": "Image ready!",
        "video_ready": "Video ready!",
        "generation_error": "Generation error",

        # Balance
        "no_api_key": "No API key",
        "loading": "Loading...",
        "data_error": "Data error",
        "error": "Error",
        "network_error": "Network error",

        # Messages
        "video_saved": "Video saved!\nClick to watch",
        "preview_here": "Preview will appear here",
        "folder_not_exist": "Folder does not exist",
        "success": "Success",
        "folder_set": "Save folder:",
        "warning": "Warning",

        # Errors
        "error_request": "Request error",
        "error_download": "Download error",
        "error_timeout": "Timeout: server did not respond",
        "error_api": "API Error",

        # Log messages
        "log_request": "Request: {model} ({id})",
        "log_done": "Done!",
        "log_error": "Error: {detail}",
        "log_error_code": "Error {code}: {detail}",
        "log_video_generating": "Generating video ({model})... This may take 1-2 minutes.",
        "log_sending_request": "Sending request to server...",
        "log_video_saved": "Video saved!",
        "log_got_link": "Got link, downloading...",
        "log_unexpected_response": "Unexpected response: {detail}",
        "log_api_error": "API Error {code}: {detail}",
        "log_timeout_3min": "Timeout: server did not respond in 3 minutes",
        "log_llm_request": "LLM request ({model})...",
        "log_done_saved": "Done! Saved: {filename}",
        "log_no_data": "No data",
        "log_reference": "Reference: {url}",
        "preview_error": "Preview error: {detail}",
        "chat_error_code": "Error {code}",
        "chat_error": "Error: {detail}",

        # Context menu
        "ctx_copy": "Copy",
        "ctx_paste": "Paste",
        "ctx_cut": "Cut",
        "ctx_select_all": "Select All",
    },
    "ru": {
        # App
        "app_title": "Pollinations Manager | AI Chat Hub Edition",
        "version": "v2.0",

        # Sidebar
        "your_balance": "ВАШ БАЛАНС",
        "pollen": "Pollen",
        "refresh": "Обновить",
        "save_folder": "Папка сохранения",
        "open_folder": "Открыть папку",
        "theme": "Тема:",
        "language": "Язык:",
        "our_telegram": "Наш Telegram",

        # Tabs
        "tab_chat": "Чат",
        "tab_images": "Изображения",
        "tab_video": "Видео",

        # Chat
        "model": "Модель:",
        "save_chat": "Сохранить",
        "clear_chat": "Очистить",
        "send": "Отправить",
        "send_hint": "Ctrl+Enter для отправки",
        "chat_welcome": "Привет! Я готов помочь. Выберите модель и напишите ваш вопрос.",
        "chat_cleared": "Чат очищен. Начните новый диалог.",
        "you": "Вы",
        "ai": "AI",
        "copied": "Скопировано!",
        "nothing_to_save": "Нечего сохранять",
        "saved": "Сохранено",
        "generating_response": "Генерация ответа...",

        # Generation
        "prompt_label": "Ваш запрос (Prompt):",
        "generate": "ГЕНЕРИРОВАТЬ",
        "generating": "Генерация... Пожалуйста подождите.",
        "size_format": "Размер и Формат:",
        "style": "Стилизация:",
        "no_style": "Без стиля",
        "duration_sec": "Длительность (сек):",
        "generate_audio": "Генерировать звук (veo)",
        "high_quality": "High Quality / 4K",
        "reference_image": "Референс изображение:",
        "select_image": "Выбрать",
        "clear_image": "Убрать",
        "no_image": "Изображение не выбрано",
        "uploading_image": "Загрузка изображения...",
        "upload_error": "Ошибка загрузки",
        "image_ready_to_use": "Изображение готово",
        "supported_models": "Поддержка: kontext, seedance, wan",

        # Status
        "ready": "Готов к работе",
        "api_online": "API Online",
        "generating_image": "Генерация изображения...",
        "generating_video": "Генерация видео...",
        "generating_text": "Генерация текста...",
        "image_ready": "Изображение готово!",
        "video_ready": "Видео готово!",
        "generation_error": "Ошибка генерации",

        # Balance
        "no_api_key": "Нет API ключа",
        "loading": "Загрузка...",
        "data_error": "Ошибка данных",
        "error": "Ошибка",
        "network_error": "Ошибка сети",

        # Messages
        "video_saved": "Видео сохранено!\nНажмите, чтобы смотреть",
        "preview_here": "Превью появится здесь",
        "folder_not_exist": "Папка не существует",
        "success": "Успех",
        "folder_set": "Папка сохранений:",
        "warning": "Внимание",

        # Errors
        "error_request": "Ошибка запроса",
        "error_download": "Ошибка скачивания",
        "error_timeout": "Таймаут: сервер не ответил",
        "error_api": "Ошибка API",

        # Log messages
        "log_request": "Запрос: {model} ({id})",
        "log_done": "Готово!",
        "log_error": "Ошибка: {detail}",
        "log_error_code": "Ошибка {code}: {detail}",
        "log_video_generating": "Генерация видео ({model})... Это может занять 1-2 минуты.",
        "log_sending_request": "Отправляю запрос на сервер...",
        "log_video_saved": "Видео сохранено!",
        "log_got_link": "Получена ссылка, скачиваю...",
        "log_unexpected_response": "Неожиданный ответ: {detail}",
        "log_api_error": "Ошибка API {code}: {detail}",
        "log_timeout_3min": "Таймаут: сервер не ответил за 3 минуты",
        "log_llm_request": "Запрос LLM ({model})...",
        "log_done_saved": "Готово! Сохранено: {filename}",
        "log_no_data": "Нет данных",
        "log_reference": "Референс: {url}",
        "preview_error": "Ошибка превью: {detail}",
        "chat_error_code": "Ошибка {code}",
        "chat_error": "Ошибка: {detail}",

        # Context menu
        "ctx_copy": "Копировать",
        "ctx_paste": "Вставить",
        "ctx_cut": "Вырезать",
        "ctx_select_all": "Выделить всё",
    },
    "de": {
        "app_title": "Pollinations Manager | AI Chat Hub Edition",
        "version": "v2.0",
        "your_balance": "IHR GUTHABEN",
        "pollen": "Pollen",
        "refresh": "Aktualisieren",
        "save_folder": "Speicherordner",
        "open_folder": "Ordner öffnen",
        "theme": "Design:",
        "language": "Sprache:",
        "our_telegram": "Unser Telegram",
        "tab_chat": "Chat",
        "tab_images": "Bilder",
        "tab_video": "Video",
        "model": "Modell:",
        "save_chat": "Speichern",
        "clear_chat": "Löschen",
        "send": "Senden",
        "send_hint": "Strg+Enter zum Senden",
        "chat_welcome": "Hallo! Ich bin bereit zu helfen. Wählen Sie ein Modell und stellen Sie Ihre Frage.",
        "chat_cleared": "Chat gelöscht. Starten Sie ein neues Gespräch.",
        "you": "Sie",
        "ai": "KI",
        "copied": "Kopiert!",
        "nothing_to_save": "Nichts zu speichern",
        "saved": "Gespeichert",
        "generating_response": "Antwort wird generiert...",
        "prompt_label": "Ihre Eingabe (Prompt):",
        "generate": "GENERIEREN",
        "generating": "Generierung... Bitte warten.",
        "size_format": "Größe und Format:",
        "style": "Stil:",
        "no_style": "Kein Stil",
        "duration_sec": "Dauer (Sek):",
        "generate_audio": "Audio generieren (veo)",
        "high_quality": "Hohe Qualität / 4K",
        "reference_image": "Referenzbild:",
        "select_image": "Auswählen",
        "clear_image": "Löschen",
        "no_image": "Kein Bild ausgewählt",
        "uploading_image": "Bild wird hochgeladen...",
        "upload_error": "Upload-Fehler",
        "image_ready_to_use": "Bild bereit",
        "supported_models": "Unterstützt: kontext, seedance, wan",
        "ready": "Bereit",
        "api_online": "API Online",
        "generating_image": "Bild wird generiert...",
        "generating_video": "Video wird generiert...",
        "generating_text": "Text wird generiert...",
        "image_ready": "Bild fertig!",
        "video_ready": "Video fertig!",
        "generation_error": "Generierungsfehler",
        "no_api_key": "Kein API-Schlüssel",
        "loading": "Laden...",
        "data_error": "Datenfehler",
        "error": "Fehler",
        "network_error": "Netzwerkfehler",
        "video_saved": "Video gespeichert!\nKlicken zum Abspielen",
        "preview_here": "Vorschau erscheint hier",
        "folder_not_exist": "Ordner existiert nicht",
        "success": "Erfolg",
        "folder_set": "Speicherordner:",
        "warning": "Warnung",
        "error_request": "Anfragefehler",
        "error_download": "Download-Fehler",
        "error_timeout": "Zeitüberschreitung",
        "error_api": "API-Fehler",
    },
    "fr": {
        "app_title": "Pollinations Manager | AI Chat Hub Edition",
        "version": "v2.0",
        "your_balance": "VOTRE SOLDE",
        "pollen": "Pollen",
        "refresh": "Actualiser",
        "save_folder": "Dossier de sauvegarde",
        "open_folder": "Ouvrir le dossier",
        "theme": "Thème:",
        "language": "Langue:",
        "our_telegram": "Notre Telegram",
        "tab_chat": "Chat",
        "tab_images": "Images",
        "tab_video": "Vidéo",
        "model": "Modèle:",
        "save_chat": "Enregistrer",
        "clear_chat": "Effacer",
        "send": "Envoyer",
        "send_hint": "Ctrl+Entrée pour envoyer",
        "chat_welcome": "Bonjour! Je suis prêt à vous aider. Choisissez un modèle et posez votre question.",
        "chat_cleared": "Chat effacé. Commencez une nouvelle conversation.",
        "you": "Vous",
        "ai": "IA",
        "copied": "Copié!",
        "nothing_to_save": "Rien à enregistrer",
        "saved": "Enregistré",
        "generating_response": "Génération de la réponse...",
        "prompt_label": "Votre requête (Prompt):",
        "generate": "GÉNÉRER",
        "generating": "Génération... Veuillez patienter.",
        "size_format": "Taille et Format:",
        "style": "Style:",
        "no_style": "Sans style",
        "duration_sec": "Durée (sec):",
        "generate_audio": "Générer l'audio (veo)",
        "high_quality": "Haute Qualité / 4K",
        "reference_image": "Image de référence:",
        "select_image": "Choisir",
        "clear_image": "Effacer",
        "no_image": "Aucune image sélectionnée",
        "uploading_image": "Téléchargement de l'image...",
        "upload_error": "Erreur de téléchargement",
        "image_ready_to_use": "Image prête",
        "supported_models": "Supporté: kontext, seedance, wan",
        "ready": "Prêt",
        "api_online": "API En ligne",
        "generating_image": "Génération de l'image...",
        "generating_video": "Génération de la vidéo...",
        "generating_text": "Génération du texte...",
        "image_ready": "Image prête!",
        "video_ready": "Vidéo prête!",
        "generation_error": "Erreur de génération",
        "no_api_key": "Pas de clé API",
        "loading": "Chargement...",
        "data_error": "Erreur de données",
        "error": "Erreur",
        "network_error": "Erreur réseau",
        "video_saved": "Vidéo enregistrée!\nCliquez pour regarder",
        "preview_here": "L'aperçu apparaîtra ici",
        "folder_not_exist": "Le dossier n'existe pas",
        "success": "Succès",
        "folder_set": "Dossier de sauvegarde:",
        "warning": "Attention",
        "error_request": "Erreur de requête",
        "error_download": "Erreur de téléchargement",
        "error_timeout": "Délai dépassé",
        "error_api": "Erreur API",
    },
    "ja": {
        "app_title": "Pollinations Manager | AI Chat Hub Edition",
        "version": "v2.0",
        "your_balance": "残高",
        "pollen": "Pollen",
        "refresh": "更新",
        "save_folder": "保存フォルダ",
        "open_folder": "フォルダを開く",
        "theme": "テーマ:",
        "language": "言語:",
        "our_telegram": "Telegram",
        "tab_chat": "チャット",
        "tab_images": "画像",
        "tab_video": "動画",
        "model": "モデル:",
        "save_chat": "保存",
        "clear_chat": "クリア",
        "send": "送信",
        "send_hint": "Ctrl+Enterで送信",
        "chat_welcome": "こんにちは！お手伝いの準備ができています。モデルを選んで質問してください。",
        "chat_cleared": "チャットをクリアしました。新しい会話を始めてください。",
        "you": "あなた",
        "ai": "AI",
        "copied": "コピーしました！",
        "nothing_to_save": "保存するものがありません",
        "saved": "保存しました",
        "generating_response": "応答を生成中...",
        "prompt_label": "プロンプト:",
        "generate": "生成",
        "generating": "生成中... お待ちください。",
        "size_format": "サイズとフォーマット:",
        "style": "スタイル:",
        "no_style": "スタイルなし",
        "duration_sec": "長さ（秒）:",
        "generate_audio": "音声を生成 (veo)",
        "high_quality": "高画質 / 4K",
        "reference_image": "参照画像:",
        "select_image": "選択",
        "clear_image": "クリア",
        "no_image": "画像が選択されていません",
        "uploading_image": "画像をアップロード中...",
        "upload_error": "アップロードエラー",
        "image_ready_to_use": "画像準備完了",
        "supported_models": "対応: kontext, seedance, wan",
        "ready": "準備完了",
        "api_online": "API オンライン",
        "generating_image": "画像を生成中...",
        "generating_video": "動画を生成中...",
        "generating_text": "テキストを生成中...",
        "image_ready": "画像完成！",
        "video_ready": "動画完成！",
        "generation_error": "生成エラー",
        "no_api_key": "APIキーがありません",
        "loading": "読み込み中...",
        "data_error": "データエラー",
        "error": "エラー",
        "network_error": "ネットワークエラー",
        "video_saved": "動画を保存しました！\nクリックして再生",
        "preview_here": "プレビューがここに表示されます",
        "folder_not_exist": "フォルダが存在しません",
        "success": "成功",
        "folder_set": "保存フォルダ:",
        "warning": "警告",
        "error_request": "リクエストエラー",
        "error_download": "ダウンロードエラー",
        "error_timeout": "タイムアウト",
        "error_api": "APIエラー",
    },
    "pt": {
        "app_title": "Pollinations Manager | AI Chat Hub Edition",
        "version": "v2.0",
        "your_balance": "SEU SALDO",
        "pollen": "Pollen",
        "refresh": "Atualizar",
        "save_folder": "Pasta de salvamento",
        "open_folder": "Abrir pasta",
        "theme": "Tema:",
        "language": "Idioma:",
        "our_telegram": "Nosso Telegram",
        "tab_chat": "Chat",
        "tab_images": "Imagens",
        "tab_video": "Vídeo",
        "model": "Modelo:",
        "save_chat": "Salvar",
        "clear_chat": "Limpar",
        "send": "Enviar",
        "send_hint": "Ctrl+Enter para enviar",
        "chat_welcome": "Olá! Estou pronto para ajudar. Escolha um modelo e faça sua pergunta.",
        "chat_cleared": "Chat limpo. Inicie uma nova conversa.",
        "you": "Você",
        "ai": "IA",
        "copied": "Copiado!",
        "nothing_to_save": "Nada para salvar",
        "saved": "Salvo",
        "generating_response": "Gerando resposta...",
        "prompt_label": "Seu prompt:",
        "generate": "GERAR",
        "generating": "Gerando... Por favor aguarde.",
        "size_format": "Tamanho e Formato:",
        "style": "Estilo:",
        "no_style": "Sem estilo",
        "duration_sec": "Duração (seg):",
        "generate_audio": "Gerar áudio (veo)",
        "high_quality": "Alta Qualidade / 4K",
        "reference_image": "Imagem de referência:",
        "select_image": "Selecionar",
        "clear_image": "Limpar",
        "no_image": "Nenhuma imagem selecionada",
        "uploading_image": "Enviando imagem...",
        "upload_error": "Erro no envio",
        "image_ready_to_use": "Imagem pronta",
        "supported_models": "Suportado: kontext, seedance, wan",
        "ready": "Pronto",
        "api_online": "API Online",
        "generating_image": "Gerando imagem...",
        "generating_video": "Gerando vídeo...",
        "generating_text": "Gerando texto...",
        "image_ready": "Imagem pronta!",
        "video_ready": "Vídeo pronto!",
        "generation_error": "Erro de geração",
        "no_api_key": "Sem chave API",
        "loading": "Carregando...",
        "data_error": "Erro de dados",
        "error": "Erro",
        "network_error": "Erro de rede",
        "video_saved": "Vídeo salvo!\nClique para assistir",
        "preview_here": "A prévia aparecerá aqui",
        "folder_not_exist": "Pasta não existe",
        "success": "Sucesso",
        "folder_set": "Pasta de salvamento:",
        "warning": "Aviso",
        "error_request": "Erro de requisição",
        "error_download": "Erro de download",
        "error_timeout": "Tempo esgotado",
        "error_api": "Erro de API",
    },
    "es": {
        "app_title": "Pollinations Manager | AI Chat Hub Edition",
        "version": "v2.0",
        "your_balance": "TU SALDO",
        "pollen": "Pollen",
        "refresh": "Actualizar",
        "save_folder": "Carpeta de guardado",
        "open_folder": "Abrir carpeta",
        "theme": "Tema:",
        "language": "Idioma:",
        "our_telegram": "Nuestro Telegram",
        "tab_chat": "Chat",
        "tab_images": "Imágenes",
        "tab_video": "Vídeo",
        "model": "Modelo:",
        "save_chat": "Guardar",
        "clear_chat": "Limpiar",
        "send": "Enviar",
        "send_hint": "Ctrl+Enter para enviar",
        "chat_welcome": "¡Hola! Estoy listo para ayudar. Elige un modelo y haz tu pregunta.",
        "chat_cleared": "Chat limpiado. Inicia una nueva conversación.",
        "you": "Tú",
        "ai": "IA",
        "copied": "¡Copiado!",
        "nothing_to_save": "Nada que guardar",
        "saved": "Guardado",
        "generating_response": "Generando respuesta...",
        "prompt_label": "Tu prompt:",
        "generate": "GENERAR",
        "generating": "Generando... Por favor espera.",
        "size_format": "Tamaño y Formato:",
        "style": "Estilo:",
        "no_style": "Sin estilo",
        "duration_sec": "Duración (seg):",
        "generate_audio": "Generar audio (veo)",
        "high_quality": "Alta Calidad / 4K",
        "reference_image": "Imagen de referencia:",
        "select_image": "Seleccionar",
        "clear_image": "Borrar",
        "no_image": "Ninguna imagen seleccionada",
        "uploading_image": "Subiendo imagen...",
        "upload_error": "Error al subir",
        "image_ready_to_use": "Imagen lista",
        "supported_models": "Soportado: kontext, seedance, wan",
        "ready": "Listo",
        "api_online": "API En línea",
        "generating_image": "Generando imagen...",
        "generating_video": "Generando vídeo...",
        "generating_text": "Generando texto...",
        "image_ready": "¡Imagen lista!",
        "video_ready": "¡Vídeo listo!",
        "generation_error": "Error de generación",
        "no_api_key": "Sin clave API",
        "loading": "Cargando...",
        "data_error": "Error de datos",
        "error": "Error",
        "network_error": "Error de red",
        "video_saved": "¡Vídeo guardado!\nClic para ver",
        "preview_here": "La vista previa aparecerá aquí",
        "folder_not_exist": "La carpeta no existe",
        "success": "Éxito",
        "folder_set": "Carpeta de guardado:",
        "warning": "Advertencia",
        "error_request": "Error de solicitud",
        "error_download": "Error de descarga",
        "error_timeout": "Tiempo agotado",
        "error_api": "Error de API",
    },
    "it": {
        "app_title": "Pollinations Manager | AI Chat Hub Edition",
        "version": "v2.0",
        "your_balance": "IL TUO SALDO",
        "pollen": "Pollen",
        "refresh": "Aggiorna",
        "save_folder": "Cartella di salvataggio",
        "open_folder": "Apri cartella",
        "theme": "Tema:",
        "language": "Lingua:",
        "our_telegram": "Il nostro Telegram",
        "tab_chat": "Chat",
        "tab_images": "Immagini",
        "tab_video": "Video",
        "model": "Modello:",
        "save_chat": "Salva",
        "clear_chat": "Cancella",
        "send": "Invia",
        "send_hint": "Ctrl+Invio per inviare",
        "chat_welcome": "Ciao! Sono pronto ad aiutarti. Scegli un modello e fai la tua domanda.",
        "chat_cleared": "Chat cancellata. Inizia una nuova conversazione.",
        "you": "Tu",
        "ai": "IA",
        "copied": "Copiato!",
        "nothing_to_save": "Niente da salvare",
        "saved": "Salvato",
        "generating_response": "Generazione risposta...",
        "prompt_label": "Il tuo prompt:",
        "generate": "GENERA",
        "generating": "Generazione... Attendere prego.",
        "size_format": "Dimensione e Formato:",
        "style": "Stile:",
        "no_style": "Senza stile",
        "duration_sec": "Durata (sec):",
        "generate_audio": "Genera audio (veo)",
        "high_quality": "Alta Qualità / 4K",
        "reference_image": "Immagine di riferimento:",
        "select_image": "Seleziona",
        "clear_image": "Cancella",
        "no_image": "Nessuna immagine selezionata",
        "uploading_image": "Caricamento immagine...",
        "upload_error": "Errore di caricamento",
        "image_ready_to_use": "Immagine pronta",
        "supported_models": "Supportato: kontext, seedance, wan",
        "ready": "Pronto",
        "api_online": "API Online",
        "generating_image": "Generazione immagine...",
        "generating_video": "Generazione video...",
        "generating_text": "Generazione testo...",
        "image_ready": "Immagine pronta!",
        "video_ready": "Video pronto!",
        "generation_error": "Errore di generazione",
        "no_api_key": "Nessuna chiave API",
        "loading": "Caricamento...",
        "data_error": "Errore dati",
        "error": "Errore",
        "network_error": "Errore di rete",
        "video_saved": "Video salvato!\nClicca per guardare",
        "preview_here": "L'anteprima apparirà qui",
        "folder_not_exist": "La cartella non esiste",
        "success": "Successo",
        "folder_set": "Cartella di salvataggio:",
        "warning": "Attenzione",
        "error_request": "Errore di richiesta",
        "error_download": "Errore di download",
        "error_timeout": "Tempo scaduto",
        "error_api": "Errore API",
    },
    "pl": {
        "app_title": "Pollinations Manager | AI Chat Hub Edition",
        "version": "v2.0",
        "your_balance": "TWOJE SALDO",
        "pollen": "Pollen",
        "refresh": "Odśwież",
        "save_folder": "Folder zapisu",
        "open_folder": "Otwórz folder",
        "theme": "Motyw:",
        "language": "Język:",
        "our_telegram": "Nasz Telegram",
        "tab_chat": "Czat",
        "tab_images": "Obrazy",
        "tab_video": "Wideo",
        "model": "Model:",
        "save_chat": "Zapisz",
        "clear_chat": "Wyczyść",
        "send": "Wyślij",
        "send_hint": "Ctrl+Enter aby wysłać",
        "chat_welcome": "Cześć! Jestem gotowy do pomocy. Wybierz model i zadaj pytanie.",
        "chat_cleared": "Czat wyczyszczony. Rozpocznij nową rozmowę.",
        "you": "Ty",
        "ai": "AI",
        "copied": "Skopiowano!",
        "nothing_to_save": "Nic do zapisania",
        "saved": "Zapisano",
        "generating_response": "Generowanie odpowiedzi...",
        "prompt_label": "Twój prompt:",
        "generate": "GENERUJ",
        "generating": "Generowanie... Proszę czekać.",
        "size_format": "Rozmiar i Format:",
        "style": "Styl:",
        "no_style": "Bez stylu",
        "duration_sec": "Czas trwania (sek):",
        "generate_audio": "Generuj dźwięk (veo)",
        "high_quality": "Wysoka Jakość / 4K",
        "reference_image": "Obraz referencyjny:",
        "select_image": "Wybierz",
        "clear_image": "Usuń",
        "no_image": "Nie wybrano obrazu",
        "uploading_image": "Przesyłanie obrazu...",
        "upload_error": "Błąd przesyłania",
        "image_ready_to_use": "Obraz gotowy",
        "supported_models": "Obsługiwane: kontext, seedance, wan",
        "ready": "Gotowy",
        "api_online": "API Online",
        "generating_image": "Generowanie obrazu...",
        "generating_video": "Generowanie wideo...",
        "generating_text": "Generowanie tekstu...",
        "image_ready": "Obraz gotowy!",
        "video_ready": "Wideo gotowe!",
        "generation_error": "Błąd generowania",
        "no_api_key": "Brak klucza API",
        "loading": "Ładowanie...",
        "data_error": "Błąd danych",
        "error": "Błąd",
        "network_error": "Błąd sieci",
        "video_saved": "Wideo zapisane!\nKliknij aby odtworzyć",
        "preview_here": "Podgląd pojawi się tutaj",
        "folder_not_exist": "Folder nie istnieje",
        "success": "Sukces",
        "folder_set": "Folder zapisu:",
        "warning": "Ostrzeżenie",
        "error_request": "Błąd żądania",
        "error_download": "Błąd pobierania",
        "error_timeout": "Przekroczono limit czasu",
        "error_api": "Błąd API",
    },
    "tr": {
        "app_title": "Pollinations Manager | AI Chat Hub Edition",
        "version": "v2.0",
        "your_balance": "BAKİYENİZ",
        "pollen": "Pollen",
        "refresh": "Yenile",
        "save_folder": "Kayıt klasörü",
        "open_folder": "Klasörü aç",
        "theme": "Tema:",
        "language": "Dil:",
        "our_telegram": "Telegram'ımız",
        "tab_chat": "Sohbet",
        "tab_images": "Görseller",
        "tab_video": "Video",
        "model": "Model:",
        "save_chat": "Kaydet",
        "clear_chat": "Temizle",
        "send": "Gönder",
        "send_hint": "Göndermek için Ctrl+Enter",
        "chat_welcome": "Merhaba! Yardıma hazırım. Bir model seçin ve sorunuzu sorun.",
        "chat_cleared": "Sohbet temizlendi. Yeni bir sohbet başlatın.",
        "you": "Siz",
        "ai": "YZ",
        "copied": "Kopyalandı!",
        "nothing_to_save": "Kaydedilecek bir şey yok",
        "saved": "Kaydedildi",
        "generating_response": "Yanıt oluşturuluyor...",
        "prompt_label": "İsteminiz (Prompt):",
        "generate": "OLUŞTUR",
        "generating": "Oluşturuluyor... Lütfen bekleyin.",
        "size_format": "Boyut ve Format:",
        "style": "Stil:",
        "no_style": "Stil yok",
        "duration_sec": "Süre (sn):",
        "generate_audio": "Ses oluştur (veo)",
        "high_quality": "Yüksek Kalite / 4K",
        "reference_image": "Referans Görsel:",
        "select_image": "Seç",
        "clear_image": "Temizle",
        "no_image": "Görsel seçilmedi",
        "uploading_image": "Görsel yükleniyor...",
        "upload_error": "Yükleme hatası",
        "image_ready_to_use": "Görsel hazır",
        "supported_models": "Desteklenen: kontext, seedance, wan",
        "ready": "Hazır",
        "api_online": "API Çevrimiçi",
        "generating_image": "Görsel oluşturuluyor...",
        "generating_video": "Video oluşturuluyor...",
        "generating_text": "Metin oluşturuluyor...",
        "image_ready": "Görsel hazır!",
        "video_ready": "Video hazır!",
        "generation_error": "Oluşturma hatası",
        "no_api_key": "API anahtarı yok",
        "loading": "Yükleniyor...",
        "data_error": "Veri hatası",
        "error": "Hata",
        "network_error": "Ağ hatası",
        "video_saved": "Video kaydedildi!\nİzlemek için tıklayın",
        "preview_here": "Önizleme burada görünecek",
        "folder_not_exist": "Klasör mevcut değil",
        "success": "Başarılı",
        "folder_set": "Kayıt klasörü:",
        "warning": "Uyarı",
        "error_request": "İstek hatası",
        "error_download": "İndirme hatası",
        "error_timeout": "Zaman aşımı",
        "error_api": "API hatası",
    },
    "ar": {
        "app_title": "Pollinations Manager | AI Chat Hub Edition",
        "version": "v2.0",
        "your_balance": "رصيدك",
        "pollen": "Pollen",
        "refresh": "تحديث",
        "save_folder": "مجلد الحفظ",
        "open_folder": "فتح المجلد",
        "theme": "السمة:",
        "language": "اللغة:",
        "our_telegram": "تيليجرام",
        "tab_chat": "الدردشة",
        "tab_images": "الصور",
        "tab_video": "الفيديو",
        "model": "النموذج:",
        "save_chat": "حفظ",
        "clear_chat": "مسح",
        "send": "إرسال",
        "send_hint": "Ctrl+Enter للإرسال",
        "chat_welcome": "مرحباً! أنا مستعد للمساعدة. اختر نموذجاً واطرح سؤالك.",
        "chat_cleared": "تم مسح الدردشة. ابدأ محادثة جديدة.",
        "you": "أنت",
        "ai": "الذكاء الاصطناعي",
        "copied": "تم النسخ!",
        "nothing_to_save": "لا شيء للحفظ",
        "saved": "تم الحفظ",
        "generating_response": "جاري إنشاء الرد...",
        "prompt_label": "الأمر (Prompt):",
        "generate": "إنشاء",
        "generating": "جاري الإنشاء... يرجى الانتظار.",
        "size_format": "الحجم والتنسيق:",
        "style": "النمط:",
        "no_style": "بدون نمط",
        "duration_sec": "المدة (ثانية):",
        "generate_audio": "إنشاء صوت (veo)",
        "high_quality": "جودة عالية / 4K",
        "reference_image": "صورة مرجعية:",
        "select_image": "اختيار",
        "clear_image": "مسح",
        "no_image": "لم يتم اختيار صورة",
        "uploading_image": "جاري رفع الصورة...",
        "upload_error": "خطأ في الرفع",
        "image_ready_to_use": "الصورة جاهزة",
        "supported_models": "مدعوم: kontext, seedance, wan",
        "ready": "جاهز",
        "api_online": "API متصل",
        "generating_image": "جاري إنشاء الصورة...",
        "generating_video": "جاري إنشاء الفيديو...",
        "generating_text": "جاري إنشاء النص...",
        "image_ready": "الصورة جاهزة!",
        "video_ready": "الفيديو جاهز!",
        "generation_error": "خطأ في الإنشاء",
        "no_api_key": "لا يوجد مفتاح API",
        "loading": "جاري التحميل...",
        "data_error": "خطأ في البيانات",
        "error": "خطأ",
        "network_error": "خطأ في الشبكة",
        "video_saved": "تم حفظ الفيديو!\nانقر للمشاهدة",
        "preview_here": "ستظهر المعاينة هنا",
        "folder_not_exist": "المجلد غير موجود",
        "success": "نجاح",
        "folder_set": "مجلد الحفظ:",
        "warning": "تحذير",
        "error_request": "خطأ في الطلب",
        "error_download": "خطأ في التحميل",
        "error_timeout": "انتهت المهلة",
        "error_api": "خطأ API",
    }
}

STYLES_TRANSLATIONS = {
    "en": ["No style", "Cinematic", "Anime", "Photorealistic", "Cyberpunk", "Oil Painting", "Digital Art", "3D Render", "Sketch", "Vintage"],
    "ru": ["Без стиля", "Кинематографичный", "Аниме", "Фотореализм", "Киберпанк", "Масляная живопись", "Цифровое искусство", "3D рендер", "Набросок", "Винтаж"],
    "de": ["Kein Stil", "Filmisch", "Anime", "Fotorealistisch", "Cyberpunk", "Ölgemälde", "Digitale Kunst", "3D Render", "Skizze", "Vintage"],
    "fr": ["Sans style", "Cinématique", "Anime", "Photoréaliste", "Cyberpunk", "Peinture à l'huile", "Art numérique", "Rendu 3D", "Croquis", "Vintage"],
    "ja": ["スタイルなし", "シネマティック", "アニメ", "フォトリアル", "サイバーパンク", "油絵", "デジタルアート", "3Dレンダー", "スケッチ", "ヴィンテージ"],
    "pt": ["Sem estilo", "Cinemático", "Anime", "Fotorrealista", "Cyberpunk", "Pintura a óleo", "Arte digital", "Render 3D", "Esboço", "Vintage"],
    "es": ["Sin estilo", "Cinemático", "Anime", "Fotorrealista", "Cyberpunk", "Pintura al óleo", "Arte digital", "Render 3D", "Boceto", "Vintage"],
    "it": ["Senza stile", "Cinematografico", "Anime", "Fotorealistico", "Cyberpunk", "Pittura a olio", "Arte digitale", "Render 3D", "Schizzo", "Vintage"],
    "pl": ["Bez stylu", "Kinowy", "Anime", "Fotorealistyczny", "Cyberpunk", "Malarstwo olejne", "Sztuka cyfrowa", "Render 3D", "Szkic", "Vintage"],
    "tr": ["Stil yok", "Sinematik", "Anime", "Fotorealistik", "Cyberpunk", "Yağlı boya", "Dijital sanat", "3D Render", "Eskiz", "Vintage"],
    "ar": ["بدون نمط", "سينمائي", "أنمي", "واقعي", "سايبربانك", "رسم زيتي", "فن رقمي", "تصيير ثلاثي الأبعاد", "رسم", "عتيق"]
}

# Language display names mapping
LANGUAGE_NAMES = {
    "en": "English",
    "ru": "Русский",
    "de": "Deutsch",
    "fr": "Français",
    "ja": "日本語",
    "pt": "Português",
    "es": "Español",
    "it": "Italiano",
    "pl": "Polski",
    "tr": "Türkçe",
    "ar": "العربية"
}

# Reverse mapping: display name -> code
LANGUAGE_CODES = {v: k for k, v in LANGUAGE_NAMES.items()}

# --- CONFIG ---

CONFIG_FILE = 'config.json'
TELEGRAM_LINK = "https://t.me/+SSC4B1Dnrlc2ZTky"

# Цены (база данных) - Display Name -> Price String
PRICING_DB = {
    "image": {
        "Flux Schnell": "🖼️ 0.0002 /img",
        "Z-Image Turbo": "🖼️ 0.0002 /img",
        "Imagen 4 (api.airforce)": "🖼️ 0.0025 /img",
        "Grok Imagine (api.airforce)": "🖼️ 0.0025 /img",
        "FLUX.2 Klein 4B": "🖼️ 0.008 /img",
        "FLUX.2 Klein 9B": "🖼️ 0.012 /img",
        "GPT Image 1 Mini": "🖼️ 8.0 /M",
        "💎 Seedream 4.0": "🖼️ 0.03 /img",
        "💎 FLUX.1 Kontext": "🖼️ 0.04 /img",
        "💎 NanoBanana": "🖼️ 30.0 /M",
        "💎 Seedream 4.5 Pro": "🖼️ 0.04 /img",
        "💎 GPT Image 1.5": "🖼️ 32.0 /M",
        "💎 NanoBanana Pro": "🖼️ 120.0 /M",
    },
    "video": {
        "Grok Video (api.airforce)": "🎬 0.003 /sec",
        "💎 LTX-2": "🎬 0.010 /sec",
        "💎 Seedance Pro-Fast": "🎬 1.0 /M",
        "💎 Wan 2.6": "🎬 0.050 /sec + 🔊 0.050 /sec",
        "Seedance Lite": "🎬 1.8 /M",
        "💎 Veo 3.1 Fast": "🎬 0.150 /sec",
    },
    "text": {
        "Amazon Nova Micro": "In: 0.04/M | Out: 0.15/M",
        "Mistral Small 3.2 24B": "In: 0.15/M | Out: 0.35/M",
        "Google Gemini 2.5 Flash Lite": "In: 0.1/M | Out: 0.4/M",
        "Qwen3 Coder 30B": "In: 0.06/M | Out: 0.22/M",
        "xAI Grok 4 Fast": "In: 0.2/M | Out: 0.5/M",
        "OpenAI GPT-5 Mini": "In: 0.15/M | Out: 0.6/M",
        "Perplexity Sonar": "In: 1.0/M | Out: 1.0/M",
        "OpenAI GPT-5 Nano": "In: 0.06/M | Out: 0.44/M",
        "Google Gemini 3 Flash": "In: 0.5/M | Out: 3.0/M",
        "DeepSeek V3.2": "In: 0.57/M | Out: 1.68/M",
        "ChickyTutor AI": "In: 0.8/M | Out: 4.0/M",
        "OpenAI GPT-4o Mini Audio": "In: 0.17/M | Out: 0.66/M",
        "MIDIjourney": "In: 2.21/M | Out: 8.81/M",
        "Perplexity Sonar Reasoning": "In: 2.0/M | Out: 8.0/M",
        "Google Gemini 2.5 Pro": "In: 1.25/M | Out: 10.0/M",
        "Moonshot Kimi K2 Thinking": "In: 0.6/M | Out: 2.5/M",
        "Z.ai GLM-4.7": "In: 0.6/M | Out: 2.21/M",
        "OpenAI GPT-5.2": "In: 1.75/M | Out: 14.0/M",
        "Anthropic Claude Haiku 4.5": "In: 1.0/M | Out: 5.0/M",
        "MiniMax M2.1": "In: 0.3/M | Out: 1.2/M",
        "Anthropic Claude Sonnet 4.5": "In: 3.0/M | Out: 15.0/M",
        "Google Gemini 3 Pro": "In: 2.0/M | Out: 12.0/M",
        "Anthropic Claude Opus 4.5": "In: 5.0/M | Out: 25.0/M",
    }
}

# Маппинг Display Name -> API Model ID
MODEL_IDS = {
    # Image models
    "Flux Schnell": "flux",
    "Z-Image Turbo": "zimage",
    "Imagen 4 (api.airforce)": "imagen-4",
    "Grok Imagine (api.airforce)": "grok-imagine",
    "FLUX.2 Klein 4B": "klein",
    "FLUX.2 Klein 9B": "klein-large",
    "GPT Image 1 Mini": "gptimage",
    "💎 Seedream 4.0": "seedream",
    "💎 FLUX.1 Kontext": "kontext",
    "💎 NanoBanana": "nanobanana",
    "💎 Seedream 4.5 Pro": "seedream-pro",
    "💎 GPT Image 1.5": "gptimage-large",
    "💎 NanoBanana Pro": "nanobanana-pro",
    # Video models
    "Grok Video (api.airforce)": "grok-video",
    "💎 LTX-2": "ltx-2",
    "💎 Seedance Pro-Fast": "seedance-pro",
    "💎 Wan 2.6": "wan",
    "Seedance Lite": "seedance",
    "💎 Veo 3.1 Fast": "veo",
    # Text models
    "Amazon Nova Micro": "amazon-nova-micro",
    "Mistral Small 3.2 24B": "mistral-small",
    "Google Gemini 2.5 Flash Lite": "gemini-2.5-flash-lite",
    "Qwen3 Coder 30B": "qwen3-coder-30b",
    "xAI Grok 4 Fast": "grok-4-fast",
    "OpenAI GPT-5 Mini": "gpt-5-mini",
    "Perplexity Sonar": "sonar",
    "OpenAI GPT-5 Nano": "gpt-5-nano",
    "Google Gemini 3 Flash": "gemini-3-flash",
    "DeepSeek V3.2": "deepseek-v3.2",
    "ChickyTutor AI": "chickytutor",
    "OpenAI GPT-4o Mini Audio": "gpt-4o-mini-audio",
    "MIDIjourney": "midijourney",
    "Perplexity Sonar Reasoning": "sonar-reasoning",
    "Google Gemini 2.5 Pro": "gemini-2.5-pro",
    "Moonshot Kimi K2 Thinking": "kimi-k2-thinking",
    "Z.ai GLM-4.7": "glm-4.7",
    "OpenAI GPT-5.2": "gpt-5.2",
    "Anthropic Claude Haiku 4.5": "claude-haiku",
    "MiniMax M2.1": "minimax-m2.1",
    "Anthropic Claude Sonnet 4.5": "claude-sonnet",
    "Google Gemini 3 Pro": "gemini-3-pro",
    "Anthropic Claude Opus 4.5": "claude-opus",
}

ASPECT_RATIOS = {
    "1:1 (Square)": (1024, 1024),
    "16:9 (Landscape)": (1280, 720),
    "9:16 (Portrait)": (720, 1280),
    "4:3 (Photo)": (1024, 768),
    "3:4 (Photo Portrait)": (768, 1024),
    "3:2 (Classic)": (1152, 768),
    "2:3 (Classic Portrait)": (768, 1152),
    "21:9 (Cinematic)": (1536, 640)
}

class PollinationsApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.load_config()

        self.title(self.t("app_title"))
        self.geometry("1100x900")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.setup_ui()
        self.after(1000, self.update_balance_display)

    def t(self, key):
        """Get translation for key"""
        return TRANSLATIONS.get(self.lang, TRANSLATIONS["en"]).get(key, key)

    def get_styles(self):
        """Get styles list for current language"""
        return STYLES_TRANSLATIONS.get(self.lang, STYLES_TRANSLATIONS["en"])

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'w') as f:
                json.dump({"api_key": "", "save_folder": "pollinations_results", "language": "en"}, f)

        try:
            with open(CONFIG_FILE, 'r') as f:
                self.config = json.load(f)
        except json.JSONDecodeError:
            self.config = {"api_key": "", "save_folder": "pollinations_results", "language": "en"}

        # Set language (default: English)
        self.lang = self.config.get('language', 'en')

        if not os.path.exists(self.config.get('save_folder', 'pollinations_results')):
            os.makedirs(self.config.get('save_folder', 'pollinations_results'))

    def save_config(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f)

    def show_context_menu(self, event, widget):
        try:
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label=self.t("ctx_copy"), command=lambda: self.copy_widget_text(widget))
            menu.add_command(label=self.t("ctx_paste"), command=lambda: self.paste_to_widget(widget))
            menu.add_command(label=self.t("ctx_cut"), command=lambda: self.cut_widget_text(widget))
            menu.add_separator()
            menu.add_command(label=self.t("ctx_select_all"), command=lambda: self.select_all_widget(widget))
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def copy_widget_text(self, widget):
        """Копирует выделенный текст в буфер обмена"""
        try:
            if isinstance(widget, ctk.CTkTextbox):
                text = widget.get("sel.first", "sel.last")
            else:
                text = widget.selection_get()
            self.clipboard_clear()
            self.clipboard_append(text)
        except Exception:
            pass

    def paste_to_widget(self, widget):
        """Вставляет текст из буфера обмена"""
        try:
            text = self.clipboard_get()
            if isinstance(widget, ctk.CTkTextbox):
                try:
                    widget.delete("sel.first", "sel.last")
                except Exception:
                    pass
                widget.insert("insert", text)
            elif isinstance(widget, ctk.CTkEntry):
                try:
                    widget.delete("sel.first", "sel.last")
                except Exception:
                    pass
                widget.insert("insert", text)
        except Exception:
            pass

    def cut_widget_text(self, widget):
        """Вырезает выделенный текст"""
        self.copy_widget_text(widget)
        try:
            if isinstance(widget, ctk.CTkTextbox):
                widget.delete("sel.first", "sel.last")
        except Exception:
            pass

    def select_all_widget(self, widget):
        """Выделяет весь текст"""
        if isinstance(widget, ctk.CTkTextbox):
            widget.tag_add("sel", "1.0", "end")

    def bind_hotkeys(self, widget):
        """Добавляет горячие клавиши для русской и английской раскладки"""
        # Используем keycode вместо символов для поддержки русской раскладки
        # V=86, C=67, X=88, A=65

        def on_key(event):
            if event.state & 0x4:  # Ctrl нажат
                if event.keycode == 86:  # V
                    self.paste_to_widget(widget)
                    return "break"
                elif event.keycode == 67:  # C
                    self.copy_widget_text(widget)
                    return "break"
                elif event.keycode == 88:  # X
                    self.cut_widget_text(widget)
                    return "break"
                elif event.keycode == 65:  # A
                    self.select_all_widget(widget)
                    return "break"

        widget.bind("<Key>", on_key)

    def setup_ui(self):
        # Основной контейнер
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self.main_container, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.logo_label = ctk.CTkLabel(self.sidebar, text="🌸 Pollinations\n    Manager", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(padx=20, pady=(20, 5))

        # Версия
        ctk.CTkLabel(self.sidebar, text="v2.0", font=("Arial", 10), text_color="gray").pack()

        # Balance
        self.balance_frame = ctk.CTkFrame(self.sidebar, fg_color=("gray85", "#252525"), border_color="#1f6aa5", border_width=2, corner_radius=10)
        self.balance_frame.pack(padx=10, pady=15, fill="x")

        ctk.CTkLabel(self.balance_frame, text=f"💰 {self.t('your_balance')}", font=("Arial", 10, "bold"), text_color="gray").pack(pady=(8, 0))
        self.balance_value = ctk.CTkLabel(self.balance_frame, text="---", font=("Arial", 24, "bold"), text_color="#4ade80")
        self.balance_value.pack(pady=(0, 2))
        ctk.CTkLabel(self.balance_frame, text=self.t("pollen"), font=("Arial", 10), text_color="gray").pack(pady=(0, 5))

        self.refresh_btn = ctk.CTkButton(self.balance_frame, text=f"🔄 {self.t('refresh')}", height=25,
                                         fg_color=("gray70", "#333"), hover_color=("gray60", "#444"),
                                         command=self.update_balance_display)
        self.refresh_btn.pack(pady=(0, 10), padx=15, fill="x")

        # Разделитель
        ctk.CTkFrame(self.sidebar, height=2, fg_color=("gray70", "#333")).pack(fill="x", padx=15, pady=10)

        # Save folder
        self.folder_btn = ctk.CTkButton(self.sidebar, text=f"📂 {self.t('save_folder')}",
                                        fg_color=("gray70", "#333"), hover_color=("gray60", "#444"),
                                        command=self.choose_folder)
        self.folder_btn.pack(padx=10, pady=5, fill="x")

        # Open folder
        self.open_folder_btn = ctk.CTkButton(self.sidebar, text=f"📁 {self.t('open_folder')}",
                                             fg_color=("gray70", "#333"), hover_color=("gray60", "#444"),
                                             command=self.open_save_folder)
        self.open_folder_btn.pack(padx=10, pady=5, fill="x")

        # Тема
        # Theme
        theme_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        theme_frame.pack(padx=10, pady=5, fill="x")
        self.theme_label = ctk.CTkLabel(theme_frame, text=self.t("theme"), font=("Arial", 11))
        self.theme_label.pack(side="left")
        self.theme_var = ctk.StringVar(value="Dark")
        theme_menu = ctk.CTkOptionMenu(theme_frame, variable=self.theme_var,
                                       values=["Dark", "Light", "System"],
                                       width=100, command=self.change_theme)
        theme_menu.pack(side="right")

        # Language
        lang_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        lang_frame.pack(padx=10, pady=5, fill="x")
        self.lang_label = ctk.CTkLabel(lang_frame, text=self.t("language"), font=("Arial", 11))
        self.lang_label.pack(side="left")
        self.lang_var = ctk.StringVar(value=LANGUAGE_NAMES.get(self.lang, "English"))
        lang_menu = ctk.CTkOptionMenu(lang_frame, variable=self.lang_var,
                                      values=list(LANGUAGE_NAMES.values()),
                                      width=120, command=self.change_language)
        lang_menu.pack(side="right")

        # Telegram
        self.tg_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.tg_frame.pack(padx=10, pady=10, side="bottom", fill="x")

        ctk.CTkLabel(self.tg_frame, text="AI Chat Hub", font=("Arial", 11, "bold")).pack(pady=(0, 5))
        self.tg_btn = ctk.CTkButton(self.tg_frame, text=f"✈️ {self.t('our_telegram')}",
                                    fg_color="#0088cc", hover_color="#006699",
                                    command=lambda: webbrowser.open(TELEGRAM_LINK))
        self.tg_btn.pack(fill="x")

        # Tabs
        self.tabview = ctk.CTkTabview(self.main_container)
        self.tabview.pack(side="right", fill="both", expand=True, padx=(0, 15), pady=10)

        self.setup_text_tab()
        self.setup_image_tab()
        self.setup_video_tab()

        # Status bar
        self.statusbar = ctk.CTkFrame(self, height=25, fg_color=("gray85", "#1a1a1a"), corner_radius=0)
        self.statusbar.pack(side="bottom", fill="x")

        self.status_label = ctk.CTkLabel(self.statusbar, text=f"✓ {self.t('ready')}",
                                         font=("Arial", 10), text_color="gray")
        self.status_label.pack(side="left", padx=10)

        self.api_status = ctk.CTkLabel(self.statusbar, text=f"🟢 {self.t('api_online')}",
                                       font=("Arial", 10), text_color="#4ade80")
        self.api_status.pack(side="right", padx=10)

    def change_theme(self, theme):
        ctk.set_appearance_mode(theme)

    def change_language(self, lang_name):
        self.lang = LANGUAGE_CODES.get(lang_name, "en")
        self.config['language'] = self.lang
        self.save_config()

        # Show restart message in the selected language
        restart_messages = {
            "en": "Language changed. Please restart the app to apply changes.",
            "ru": "Язык изменён. Перезапустите приложение для применения изменений.",
            "de": "Sprache geändert. Bitte starten Sie die App neu, um die Änderungen anzuwenden.",
            "fr": "Langue modifiée. Veuillez redémarrer l'application pour appliquer les changements.",
            "ja": "言語が変更されました。変更を適用するにはアプリを再起動してください。",
            "pt": "Idioma alterado. Reinicie o aplicativo para aplicar as alterações.",
            "es": "Idioma cambiado. Reinicie la aplicación para aplicar los cambios.",
            "it": "Lingua cambiata. Riavvia l'app per applicare le modifiche.",
            "pl": "Język zmieniony. Uruchom ponownie aplikację, aby zastosować zmiany.",
            "tr": "Dil değiştirildi. Değişiklikleri uygulamak için uygulamayı yeniden başlatın.",
            "ar": "تم تغيير اللغة. يرجى إعادة تشغيل التطبيق لتطبيق التغييرات."
        }
        msg = restart_messages.get(self.lang, restart_messages["en"])
        messagebox.showinfo("Info", msg)

    def open_save_folder(self):
        folder = self.config.get('save_folder', 'pollinations_results')
        if os.path.exists(folder):
            open_file_or_folder(folder)
        else:
            messagebox.showwarning(self.t("warning"), self.t("folder_not_exist"))

    def setup_text_tab(self):
        tab = self.tabview.add(f"💬 {self.t('tab_chat')}")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        # === Верхняя панель: модель + цена ===
        top_frame = ctk.CTkFrame(tab, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        ctk.CTkLabel(top_frame, text=self.t("model"), font=("Arial", 12)).pack(side="left", padx=5)
        self.chat_model_var = ctk.StringVar(value=list(PRICING_DB["text"].keys())[0])
        model_menu = ctk.CTkOptionMenu(top_frame, variable=self.chat_model_var,
                                       values=list(PRICING_DB["text"].keys()), width=220,
                                       command=self.update_chat_price)
        model_menu.pack(side="left", padx=5)

        self.chat_price_label = ctk.CTkLabel(top_frame, text=PRICING_DB["text"][self.chat_model_var.get()],
                                             text_color="#FFD700", font=("Arial", 11))
        self.chat_price_label.pack(side="left", padx=15)

        # Control buttons
        self.save_chat_btn = ctk.CTkButton(top_frame, text=f"💾 {self.t('save_chat')}", width=100,
                                           fg_color=("#4a9f4a", "#2d5a27"), hover_color=("#3d8a3d", "#3d7a37"),
                                           command=self.save_chat)
        self.save_chat_btn.pack(side="right", padx=5)

        self.clear_chat_btn = ctk.CTkButton(top_frame, text=f"🗑️ {self.t('clear_chat')}", width=100,
                                            fg_color=("#c75050", "#5a2727"), hover_color=("#b04040", "#7a3737"),
                                            command=self.clear_chat)
        self.clear_chat_btn.pack(side="right", padx=5)

        # === Chat area ===
        self.chat_frame = ctk.CTkScrollableFrame(tab, fg_color=("gray90", "#1a1a1a"))
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Welcome message
        self.chat_messages = []
        self.add_chat_message("assistant", self.t("chat_welcome"))

        # === Нижняя панель: ввод + отправка ===
        bottom_frame = ctk.CTkFrame(tab, fg_color="transparent")
        bottom_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=10)
        bottom_frame.grid_columnconfigure(0, weight=1)

        self.chat_input = ctk.CTkTextbox(bottom_frame, height=100, font=("Arial", 12))
        self.chat_input.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.chat_input.bind("<Control-Return>", lambda e: self.send_chat_message())
        self.chat_input.bind("<Button-3>", lambda e: self.show_context_menu(e, self.chat_input))
        self.bind_hotkeys(self.chat_input)

        btn_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=1)

        self.send_btn = ctk.CTkButton(btn_frame, text=f"📤 {self.t('send')}", width=110, height=50,
                                      font=("Arial", 13, "bold"),
                                      command=self.send_chat_message)
        self.send_btn.pack(pady=2)

        # Hint
        hint_label = ctk.CTkLabel(bottom_frame, text=self.t("send_hint"),
                                  font=("Arial", 9), text_color="gray")
        hint_label.grid(row=1, column=0, sticky="w")

        # Статус
        self.chat_status = ctk.CTkLabel(bottom_frame, text="", font=("Arial", 10), text_color="gray")
        self.chat_status.grid(row=1, column=1, sticky="e")

    def update_chat_price(self, choice):
        price = PRICING_DB["text"].get(choice, "")
        self.chat_price_label.configure(text=price)

    def add_chat_message(self, role, content):
        """Add message to chat"""
        self.chat_messages.append({"role": role, "content": content})

        # Create message frame
        if role == "user":
            msg_frame = ctk.CTkFrame(self.chat_frame, fg_color=("#cce0ff", "#2b4a6b"), corner_radius=10)
            prefix = f"👤 {self.t('you')}"
            anchor = "e"
        else:
            msg_frame = ctk.CTkFrame(self.chat_frame, fg_color=("#e8e8e8", "#2b2b2b"), corner_radius=10)
            prefix = f"🤖 {self.t('ai')}"
            anchor = "w"

        msg_frame.pack(fill="x", padx=10, pady=5, anchor=anchor)

        # Заголовок
        header = ctk.CTkLabel(msg_frame, text=prefix, font=("Arial", 10, "bold"), text_color=("gray40", "gray60"))
        header.pack(anchor="w", padx=10, pady=(5, 0))

        # Текст сообщения
        msg_text = ctk.CTkLabel(msg_frame, text=content, font=("Arial", 12),
                                wraplength=600, justify="left", anchor="w",
                                text_color=("gray10", "gray90"))
        msg_text.pack(fill="x", padx=10, pady=(2, 8))

        # Кнопка копирования для ответов AI (skip welcome/cleared messages in all languages)
        skip_texts = set()
        for lang_data in TRANSLATIONS.values():
            skip_texts.add(lang_data.get("chat_welcome", ""))
            skip_texts.add(lang_data.get("chat_cleared", ""))
        if role == "assistant" and content not in skip_texts:
            copy_btn = ctk.CTkButton(msg_frame, text="📋", width=30, height=20,
                                     fg_color="transparent", hover_color=("gray70", "#444"),
                                     command=lambda c=content: self.copy_to_clipboard(c))
            copy_btn.pack(anchor="e", padx=5, pady=(0, 5))

        # Прокрутка вниз
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    def copy_to_clipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        self.chat_status.configure(text=f"✓ {self.t('copied')}", text_color="#4ade80")
        self.after(2000, lambda: self.chat_status.configure(text="", text_color="gray"))

    def clear_chat(self):
        """Clear chat history"""
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self.chat_messages = []
        self.add_chat_message("assistant", self.t("chat_cleared"))

    def save_chat(self):
        """Save chat to file"""
        if len(self.chat_messages) <= 1:
            self.chat_status.configure(text=self.t("nothing_to_save"), text_color="orange")
            self.after(2000, lambda: self.chat_status.configure(text=""))
            return

        save_path = self.config.get('save_folder', 'pollinations_results')
        filename = f"{save_path}/chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"=== Chat {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")
            f.write(f"Model: {self.chat_model_var.get()}\n\n")
            for msg in self.chat_messages:
                role = self.t("you") if msg["role"] == "user" else self.t("ai")
                f.write(f"[{role}]\n{msg['content']}\n\n")

        self.chat_status.configure(text=f"✓ {self.t('saved')}", text_color="#4ade80")
        self.after(3000, lambda: self.chat_status.configure(text=""))

    def send_chat_message(self):
        """Отправляет сообщение в чат"""
        prompt = self.chat_input.get("0.0", "end").strip()
        if not prompt:
            return

        # Очищаем поле ввода
        self.chat_input.delete("0.0", "end")

        # Добавляем сообщение пользователя
        self.add_chat_message("user", prompt)

        # Disable button
        self.send_btn.configure(state="disabled", text="⏳...")
        self.chat_status.configure(text=self.t("generating_response"), text_color="#FFD700")

        # Запускаем запрос в отдельном потоке
        threading.Thread(target=self.process_chat_request, args=(prompt,), daemon=True).start()

    def process_chat_request(self, prompt):
        """Обрабатывает запрос к LLM"""
        api_key = self.config.get("api_key")
        display_model = self.chat_model_var.get()
        model = MODEL_IDS.get(display_model, display_model)

        try:
            url = "https://gen.pollinations.ai/v1/chat/completions"
            headers = {"Content-Type": "application/json"}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"

            # Собираем историю (последние 10 сообщений для контекста)
            messages = []
            for msg in self.chat_messages[-10:]:
                messages.append({"role": msg["role"], "content": msg["content"]})

            payload = {
                "model": model,
                "messages": messages,
                "temperature": 0.7
            }

            response = requests.post(url, json=payload, headers=headers, timeout=120)

            if response.status_code == 200:
                content = response.text
                try:
                    json_resp = response.json()
                    if 'choices' in json_resp:
                        content = json_resp['choices'][0]['message']['content']
                    elif 'output' in json_resp:
                        content = json_resp['output']
                except Exception:
                    pass

                self.after(0, lambda: self.add_chat_message("assistant", content))
                self.after(0, lambda: self.chat_status.configure(text="", text_color="gray"))
                self.after(2000, self.update_balance_display)
            else:
                error = self.t("chat_error_code").format(code=response.status_code)
                self.after(0, lambda: self.add_chat_message("assistant", f"❌ {error}"))
                self.after(0, lambda: self.chat_status.configure(text=error, text_color="red"))

        except Exception as e:
            error_msg = self.t("chat_error").format(detail=e)
            self.after(0, lambda: self.add_chat_message("assistant", f"❌ {error_msg}"))
            self.after(0, lambda: self.chat_status.configure(text=str(e), text_color="red"))

        finally:
            self.after(0, lambda: self.send_btn.configure(state="normal", text=f"📤 {self.t('send')}"))

    def setup_image_tab(self):
        tab = self.tabview.add(f"🖼️ {self.t('tab_images')}")
        controls = self.setup_generic_tab(tab, "image", PRICING_DB["image"], return_controls=True)
        self.add_image_controls(controls, "image")

    def setup_video_tab(self):
        tab = self.tabview.add(f"🎬 {self.t('tab_video')}")
        controls = self.setup_generic_tab(tab, "video", PRICING_DB["video"], return_controls=True)
        self.add_image_controls(controls, "video") 

    def add_image_controls(self, controls, type_key):
        ctk.CTkLabel(controls, text=self.t("size_format"), font=("Arial", 12, "bold")).pack(pady=(10, 5), anchor="w")

        if not hasattr(self, 'ratio_vars'):
            self.ratio_vars = {}

        var = ctk.StringVar(value="1:1 (Square)")
        self.ratio_vars[type_key] = var

        menu = ctk.CTkOptionMenu(controls, variable=var, values=list(ASPECT_RATIOS.keys()),
                                 command=lambda c, t=type_key: self.on_ratio_change(c, t))
        menu.pack(fill="x", pady=5)

        size_frame = ctk.CTkFrame(controls, fg_color="transparent")
        size_frame.pack(fill="x")

        if not hasattr(self, 'size_entries'):
            self.size_entries = {}

        entry_w = ctk.CTkEntry(size_frame, placeholder_text="W", width=60)
        entry_w.pack(side="left", padx=2)
        entry_h = ctk.CTkEntry(size_frame, placeholder_text="H", width=60)
        entry_h.pack(side="left", padx=2)

        self.size_entries[type_key] = (entry_w, entry_h)
        self.on_ratio_change("1:1 (Square)", type_key)

        if type_key == "image":
            ctk.CTkLabel(controls, text=self.t("style"), font=("Arial", 12, "bold")).pack(pady=(15, 5), anchor="w")
            styles = self.get_styles()
            self.style_var = ctk.StringVar(value=styles[0])
            self.style_menu = ctk.CTkOptionMenu(controls, variable=self.style_var, values=styles)
            self.style_menu.pack(fill="x", pady=5)

            self.hq_var = ctk.BooleanVar(value=False)
            self.hq_check = ctk.CTkCheckBox(controls, text=self.t("high_quality"), variable=self.hq_var)
            self.hq_check.pack(pady=5, anchor="w")

        if type_key == "video":
            ctk.CTkLabel(controls, text=self.t("duration_sec"), font=("Arial", 12, "bold")).pack(pady=(15, 5), anchor="w")
            self.video_duration_var = ctk.StringVar(value="5")
            duration_menu = ctk.CTkOptionMenu(controls, variable=self.video_duration_var,
                                             values=["2", "3", "4", "5", "6", "8", "10"])
            duration_menu.pack(fill="x", pady=5)

            self.video_audio_var = ctk.BooleanVar(value=True)
            audio_check = ctk.CTkCheckBox(controls, text=self.t("generate_audio"), variable=self.video_audio_var)
            audio_check.pack(pady=5, anchor="w")

        # Reference Image Section (for image-to-image and image-to-video)
        ctk.CTkLabel(controls, text=self.t("reference_image"), font=("Arial", 12, "bold")).pack(pady=(15, 5), anchor="w")
        ctk.CTkLabel(controls, text=self.t("supported_models"), font=("Arial", 9), text_color="gray").pack(anchor="w")

        # Store reference image data
        if not hasattr(self, 'ref_image_urls'):
            self.ref_image_urls = {}
        if not hasattr(self, 'ref_image_labels'):
            self.ref_image_labels = {}
        if not hasattr(self, 'ref_image_previews'):
            self.ref_image_previews = {}

        self.ref_image_urls[type_key] = None

        # Button frame
        ref_btn_frame = ctk.CTkFrame(controls, fg_color="transparent")
        ref_btn_frame.pack(fill="x", pady=5)

        select_btn = ctk.CTkButton(ref_btn_frame, text=f"📁 {self.t('select_image')}", width=100,
                                   command=lambda t=type_key: self.select_reference_image(t))
        select_btn.pack(side="left", padx=(0, 5))

        clear_btn = ctk.CTkButton(ref_btn_frame, text=f"✕ {self.t('clear_image')}", width=80,
                                  fg_color="gray", hover_color="#555555",
                                  command=lambda t=type_key: self.clear_reference_image(t))
        clear_btn.pack(side="left")

        # Status label
        status_label = ctk.CTkLabel(controls, text=self.t("no_image"), text_color="gray", font=("Arial", 10))
        status_label.pack(anchor="w")
        self.ref_image_labels[type_key] = status_label

        # Preview frame
        preview_frame = ctk.CTkFrame(controls, height=80, fg_color=("gray85", "#2a2a2a"))
        preview_frame.pack(fill="x", pady=5)
        preview_frame.pack_propagate(False)

        preview_label = ctk.CTkLabel(preview_frame, text="")
        preview_label.pack(expand=True)
        self.ref_image_previews[type_key] = preview_label

    def select_reference_image(self, type_key):
        """Select and upload reference image"""
        file_path = filedialog.askopenfilename(
            title=self.t("select_image"),
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.gif"), ("All files", "*.*")]
        )

        if not file_path:
            return

        # Update status
        self.ref_image_labels[type_key].configure(text=self.t("uploading_image"), text_color="orange")
        self.update()

        # Upload in thread
        def upload_thread():
            url = upload_image_to_hosting(file_path)

            if url:
                self.ref_image_urls[type_key] = url
                self.after(0, lambda: self.ref_image_labels[type_key].configure(
                    text=f"✓ {self.t('image_ready_to_use')}", text_color="#4ade80"))

                # Show preview on main thread
                def show_preview():
                    try:
                        img = Image.open(file_path)
                        img.thumbnail((120, 70))
                        photo = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
                        # Store reference to prevent garbage collection
                        if not hasattr(self, '_ref_photos'):
                            self._ref_photos = {}
                        self._ref_photos[type_key] = photo
                        # Update label
                        preview_label = self.ref_image_previews[type_key]
                        preview_label.configure(image=photo)
                        preview_label.configure(text="")
                    except Exception as e:
                        print(f"Preview error: {e}")

                self.after(10, show_preview)
            else:
                self.ref_image_urls[type_key] = None
                self.after(0, lambda: self.ref_image_labels[type_key].configure(
                    text=f"✕ {self.t('upload_error')}", text_color="red"))

        threading.Thread(target=upload_thread, daemon=True).start()

    def clear_reference_image(self, type_key):
        """Clear reference image"""
        self.ref_image_urls[type_key] = None
        self.ref_image_labels[type_key].configure(text=self.t("no_image"), text_color="gray")
        # Clear preview
        if hasattr(self, '_ref_photos') and type_key in self._ref_photos:
            del self._ref_photos[type_key]
        try:
            self.ref_image_previews[type_key].configure(image="", text="")
        except Exception:
            pass

    def on_ratio_change(self, choice, type_key):
        w, h = ASPECT_RATIOS[choice]
        entry_w, entry_h = self.size_entries[type_key]
        entry_w.delete(0, "end")
        entry_w.insert(0, str(w))
        entry_h.delete(0, "end")
        entry_h.insert(0, str(h))

    def setup_generic_tab(self, parent, type_key, models_dict, return_controls=False):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(4, weight=1)

        # 1. Model
        top_frame = ctk.CTkFrame(parent, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        ctk.CTkLabel(top_frame, text=self.t("model")).pack(side="left", padx=5)
        model_var = ctk.StringVar(value=list(models_dict.keys())[0])
        model_dropdown = ctk.CTkOptionMenu(top_frame, variable=model_var, values=list(models_dict.keys()),
                                         width=200,
                                         command=lambda choice: self.update_price_label(choice, type_key, price_label))
        model_dropdown.pack(side="left", padx=5)
        price_label = ctk.CTkLabel(top_frame, text=models_dict[model_var.get()], text_color="#FFD700")
        price_label.pack(side="left", padx=15)

        # 2. Prompt
        prompt_label = ctk.CTkLabel(parent, text=self.t("prompt_label"), anchor="w")
        prompt_label.grid(row=1, column=0, sticky="w", padx=10, pady=(5, 0))

        prompt_entry = ctk.CTkTextbox(parent, height=120)
        prompt_entry.grid(row=2, column=0, sticky="new", padx=10, pady=5)
        prompt_entry.bind("<Button-3>", lambda event: self.show_context_menu(event, prompt_entry))
        self.bind_hotkeys(prompt_entry)

        # 3. Button
        gen_btn = ctk.CTkButton(parent, text=f"🚀 {self.t('generate')}", height=40, font=("Arial", 14, "bold"),
                              command=lambda: self.start_generation(type_key, model_var.get(), prompt_entry.get("0.0", "end")))
        gen_btn.grid(row=3, column=0, sticky="ew", padx=10, pady=10)

        # 4. Preview Area
        preview_frame = ctk.CTkFrame(parent, height=350, fg_color=("gray90", "#1a1a1a"))  # Превью
        preview_frame.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)
        preview_frame.pack_propagate(False)

        # Лейбл-заглушка или для фото
        preview_label = ctk.CTkLabel(preview_frame, text=self.t("preview_here"), text_color="gray")
        preview_label.pack(expand=True, fill="both")

        # 5. Log
        log_box = ctk.CTkTextbox(parent, height=60, state="disabled")
        log_box.grid(row=5, column=0, sticky="ew", padx=10, pady=5)
        log_box.bind("<Button-3>", lambda event: self.show_context_menu(event, log_box))

        if not hasattr(self, 'widgets'): self.widgets = {}
        self.widgets[type_key] = {
            "model": model_var,
            "prompt": prompt_entry,
            "log": log_box,
            "preview_label": preview_label,
            "preview_frame": preview_frame,
        }

        if return_controls:
            controls_frame = ctk.CTkFrame(parent, width=200)
            controls_frame.grid(row=0, column=1, rowspan=6, sticky="ns", padx=10, pady=10)
            return controls_frame

    def update_price_label(self, choice, type_key, label_widget):
        price = PRICING_DB[type_key].get(choice, "Unknown")
        label_widget.configure(text=price)

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.config['save_folder'] = folder
            self.save_config()
            messagebox.showinfo(self.t("success"), f"{self.t('folder_set')} {folder}")

    def update_balance_display(self):
        api_key = self.config.get("api_key")
        if not api_key:
            self.balance_value.configure(text=self.t("no_api_key"), text_color="red")
            return

        self.balance_value.configure(text=self.t("loading"), text_color="gray")

        def fetch():
            try:
                url = "https://gen.pollinations.ai/account/balance"
                response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
                if response.status_code == 200:
                    try:
                        data = response.json()
                        balance_raw = data.get('balance', 0)
                        try:
                            balance = f"{float(balance_raw):.2f}"
                        except (ValueError, TypeError):
                            balance = str(balance_raw)
                        self.after(0, lambda b=balance: self.balance_value.configure(text=f"{b}", text_color="#4ade80"))
                    except Exception:
                        self.after(0, lambda: self.balance_value.configure(text=self.t("data_error"), text_color="orange"))
                else:
                    self.after(0, lambda: self.balance_value.configure(text=self.t("error"), text_color="red"))
            except Exception:
                self.after(0, lambda: self.balance_value.configure(text=self.t("network_error"), text_color="red"))

        threading.Thread(target=fetch, daemon=True).start()

    def log(self, type_key, message):
        box = self.widgets[type_key]["log"]
        box.configure(state="normal")
        box.insert("end", f"[{datetime.now().strftime('%H:%M')}] {message}\n")
        box.see("end")
        box.configure(state="disabled")

    def display_text_preview(self, type_key, text):
        """Показывает текстовый ответ в области превью"""
        preview_frame = self.widgets[type_key]["preview_frame"]
        preview_label = self.widgets[type_key]["preview_label"]

        # Скрываем label и создаём текстовое поле
        preview_label.pack_forget()

        # Удаляем старый текстбокс если есть
        for widget in preview_frame.winfo_children():
            if isinstance(widget, ctk.CTkTextbox):
                widget.destroy()

        # Создаём новый текстбокс для ответа
        text_display = ctk.CTkTextbox(preview_frame, wrap="word", font=("Arial", 12))
        text_display.pack(expand=True, fill="both", padx=5, pady=5)
        text_display.insert("0.0", text)
        text_display.configure(state="disabled")
        text_display.bind("<Button-3>", lambda event: self.show_context_menu(event, text_display))

    def display_preview(self, type_key, file_path=None, is_video=False):
        label = self.widgets[type_key]["preview_label"]

        # Очистка ссылки на изображение
        if hasattr(label, '_current_image'):
            label._current_image = None
        label.configure(text="")
        
        if is_video and file_path:
            # Для видео показываем большую кнопку
            label.configure(text=f"🎬 {self.t('video_saved')}", font=("Arial", 20, "bold"), cursor="hand2")
            label.pack(expand=True, fill="both")
            label.bind("<Button-1>", lambda e: open_file_or_folder(file_path))

        elif file_path:
            # Фото
            try:
                img_data = Image.open(file_path)
                # Подгонка размера
                base_height = 340
                h_percent = (base_height / float(img_data.size[1]))
                w_size = int((float(img_data.size[0]) * float(h_percent)))
                ctk_img = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=(w_size, base_height))
                
                label.configure(image=ctk_img, text="")
                label.bind("<Button-1>", lambda e: open_file_or_folder(file_path))
                label.configure(cursor="hand2")
                label.pack(expand=True, fill="both")
            except Exception as e:
                label.configure(text=self.t("preview_error").format(detail=e), image=None)
                label.pack()

    def start_generation(self, type_key, model, prompt):
        preview_frame = self.widgets[type_key]["preview_frame"]
        lbl = self.widgets[type_key]["preview_label"]

        # Удаляем старые виджеты (текстбоксы от предыдущих ответов)
        for widget in preview_frame.winfo_children():
            if isinstance(widget, ctk.CTkTextbox):
                widget.destroy()

        # Сбрасываем ссылку на изображение
        if hasattr(lbl, '_current_image'):
            lbl._current_image = None
        lbl.pack(expand=True, fill="both")
        lbl.configure(text=f"⏳ {self.t('generating')}", font=("Arial", 14), cursor="")
        lbl.unbind("<Button-1>")

        # Update status bar
        status_keys = {"image": "generating_image", "video": "generating_video", "text": "generating_text"}
        self.status_label.configure(text=f"⏳ {self.t(status_keys.get(type_key, 'generating'))}", text_color="#FFD700")

        threading.Thread(target=self.run_api_request, args=(type_key, model, prompt), daemon=True).start()

    def run_api_request(self, type_key, display_model, prompt):
        final_prompt = prompt.strip()
        save_path = self.config.get('save_folder', 'pollinations_results')
        api_key = self.config.get("api_key")

        # Конвертируем display name в API model ID
        model = MODEL_IDS.get(display_model, display_model)

        width, height = 1024, 1024
        if type_key in ["image", "video"] and hasattr(self, 'size_entries'):
            try:
                ew, eh = self.size_entries[type_key]
                w_val = int(ew.get())
                h_val = int(eh.get())
                # Clamp to reasonable bounds
                width = max(64, min(4096, w_val))
                height = max(64, min(4096, h_val))
            except (ValueError, TypeError, KeyError):
                pass

        try:
            # === IMAGE GENERATION (GET) ===
            if type_key == "image":
                styles = []
                if hasattr(self, 'style_var'):
                    selected_style = self.style_var.get()
                    # Check if not "No style" (first item in styles list)
                    if selected_style != self.get_styles()[0]:
                        styles.append(selected_style.split(" (")[0])
                if hasattr(self, 'hq_var') and self.hq_var.get():
                    styles.append("high quality, 4k, 8k, highly detailed, photorealistic")
                if styles:
                    final_prompt += ", " + ", ".join(styles)

                self.log(type_key, self.t("log_request").format(model=display_model, id=model))
                clean_prompt = requests.utils.quote(final_prompt)
                seed = random.randint(0, 1000000000)

                # Собираем параметры
                params = f"model={model}&width={width}&height={height}&seed={seed}&nologo=true"
                if api_key:
                    params += f"&token={api_key}"

                # Add reference image if provided (for kontext and other models)
                if hasattr(self, 'ref_image_urls') and self.ref_image_urls.get("image"):
                    ref_url = self.ref_image_urls["image"]
                    # URL encode but preserve :/ for the URL structure
                    encoded_ref = requests.utils.quote(ref_url, safe=':/')
                    params += f"&image={encoded_ref}"
                    self.log(type_key, self.t("log_reference").format(url=ref_url))

                req_url = f"https://gen.pollinations.ai/image/{clean_prompt}?{params}"
                print(f"[DEBUG] Request URL: {req_url[:200]}...")

                # Добавляем заголовок авторизации
                headers = {}
                if api_key:
                    headers["Authorization"] = f"Bearer {api_key}"

                try:
                    response = requests.get(req_url, headers=headers, timeout=180)
                    if response.status_code == 200:
                        filename = f"{save_path}/img_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                        with open(filename, 'wb') as f:
                            f.write(response.content)
                        self.log(type_key, self.t("log_done"))
                        self.after(0, lambda: self.display_preview("image", filename))
                        self.after(0, lambda: self.status_label.configure(text=f"✓ {self.t('image_ready')}", text_color="#4ade80"))
                        self.after(2000, self.update_balance_display)
                        self.after(5000, lambda: self.status_label.configure(text=f"✓ {self.t('ready')}", text_color="gray"))
                    else:
                        self.log(type_key, self.t("log_error").format(detail=response.text))
                except requests.exceptions.Timeout:
                    self.log(type_key, self.t("error_timeout"))
                    self.after(0, lambda: self.status_label.configure(text=f"❌ {self.t('error_timeout')}", text_color="red"))
                    self.after(5000, lambda: self.status_label.configure(text=f"✓ {self.t('ready')}", text_color="gray"))

            # === ГЕНЕРАЦИЯ ВИДЕО (GET) ===
            elif type_key == "video":
                self.log(type_key, self.t("log_video_generating").format(model=display_model))

                # Определяем aspect ratio
                if width > height:
                    aspect = "16:9"
                elif height > width:
                    aspect = "9:16"
                else:
                    aspect = "16:9"

                # Видео генерация использует тот же image endpoint с video моделью
                clean_prompt = requests.utils.quote(final_prompt)
                seed = random.randint(0, 1000000000)

                # Параметры для видео
                params = {
                    "model": model,
                    "seed": seed,
                    "nologo": "true",
                    "aspectRatio": aspect,
                }

                # Длительность из настроек
                duration = "5"
                if hasattr(self, 'video_duration_var'):
                    duration = self.video_duration_var.get()
                params["duration"] = duration

                # veo поддерживает audio
                if model == "veo" and hasattr(self, 'video_audio_var') and self.video_audio_var.get():
                    params["audio"] = "true"

                if api_key:
                    params["token"] = api_key

                # Add reference image for image-to-video (seedance, wan support this)
                if hasattr(self, 'ref_image_urls') and self.ref_image_urls.get("video"):
                    params["image"] = self.ref_image_urls["video"]
                    self.log(type_key, self.t("log_reference").format(url=self.ref_image_urls['video']))

                # Encode params, but preserve :/ in URLs
                def encode_param(v):
                    s = str(v)
                    if s.startswith("http"):
                        return requests.utils.quote(s, safe=':/')
                    return requests.utils.quote(s, safe='')

                param_str = "&".join([f"{k}={encode_param(v)}" for k, v in params.items()])
                req_url = f"https://gen.pollinations.ai/image/{clean_prompt}?{param_str}"
                print(f"[DEBUG] Video request URL: {req_url[:200]}...")

                # Заголовок авторизации
                headers = {}
                if api_key:
                    headers["Authorization"] = f"Bearer {api_key}"

                self.log(type_key, self.t("log_sending_request"))

                try:
                    response = requests.get(req_url, headers=headers, timeout=180)  # 3 минуты таймаут для видео

                    if response.status_code == 200:
                        content_type = response.headers.get('content-type', '')

                        if 'video' in content_type or len(response.content) > 500000:
                            # Это видео файл
                            filename = f"{save_path}/video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
                            with open(filename, 'wb') as f:
                                f.write(response.content)
                            self.log(type_key, self.t("log_video_saved"))
                            self.after(0, lambda: self.display_preview("video", filename, is_video=True))
                            self.after(0, lambda: self.status_label.configure(text=f"✓ {self.t('video_ready')}", text_color="#4ade80"))
                            self.after(5000, lambda: self.status_label.configure(text=f"✓ {self.t('ready')}", text_color="gray"))
                        else:
                            # Возможно это ссылка на видео
                            content = response.text.strip()
                            if content.startswith("http"):
                                self.log(type_key, self.t("log_got_link"))
                                vid_resp = requests.get(content, timeout=120)
                                if vid_resp.status_code == 200:
                                    filename = f"{save_path}/video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
                                    with open(filename, 'wb') as f:
                                        f.write(vid_resp.content)
                                    self.log(type_key, self.t("log_video_saved"))
                                    self.after(0, lambda: self.display_preview("video", filename, is_video=True))
                                else:
                                    self.log(type_key, self.t("log_error_code").format(code=vid_resp.status_code, detail=self.t("error_download")))
                            else:
                                self.log(type_key, self.t("log_unexpected_response").format(detail=content[:100]))

                        self.after(2000, self.update_balance_display)
                    else:
                        self.log(type_key, self.t("log_api_error").format(code=response.status_code, detail=response.text[:200]))
                except requests.exceptions.Timeout:
                    self.log(type_key, self.t("log_timeout_3min"))
                except Exception as e:
                    self.log(type_key, self.t("log_error").format(detail=e))

            # === ТЕКСТ (POST) ===
            elif type_key == "text":
                self.log(type_key, self.t("log_llm_request").format(model=display_model))
                url_text = "https://gen.pollinations.ai/v1/chat/completions"
                headers = {"Content-Type": "application/json"}
                if api_key:
                    headers["Authorization"] = f"Bearer {api_key}"
                payload = {
                    "model": model,
                    "messages": [{"role": "user", "content": final_prompt}],
                    "temperature": 0.7
                }
                response = requests.post(url_text, json=payload, headers=headers)
                if response.status_code == 200:
                    content = response.text
                    try:
                        json_resp = response.json()
                        if 'choices' in json_resp:
                            content = json_resp['choices'][0]['message']['content']
                        elif 'output' in json_resp:
                            content = json_resp['output']
                    except (ValueError, KeyError, IndexError):
                        pass

                    filename = f"{save_path}/text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(content)

                    # Показываем ответ в области превью
                    self.after(0, lambda c=content: self.display_text_preview(type_key, c))
                    self.log(type_key, self.t("log_done_saved").format(filename=filename))
                    self.after(2000, self.update_balance_display)
                else:
                    error_text = response.text[:300] if response.text else self.t("log_no_data")
                    self.log(type_key, self.t("log_error_code").format(code=response.status_code, detail=error_text))

        except Exception as e:
            self.log(type_key, self.t("log_error").format(detail=e))
            self.after(0, lambda: self.status_label.configure(text=f"❌ {self.t('generation_error')}", text_color="red"))
            self.after(5000, lambda: self.status_label.configure(text=f"✓ {self.t('ready')}", text_color="gray"))
            print(e)

if __name__ == "__main__":
    app = PollinationsApp()
    app.mainloop()