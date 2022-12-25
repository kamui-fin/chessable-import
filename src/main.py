import os
import sys
import pathlib
import chess.pgn
import argparse
import pyperclip as pc
from urllib.parse import quote_plus
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint

def die(msg):
    print(msg, file=sys.stderr)
    exit(-1)

def login(username, password):
    driver.get("https://www.chessable.com/login")
    form = driver.find_element(By.CSS_SELECTOR, "form[data-test-id=loginForm]")
    email_field = form.find_element(By.CSS_SELECTOR, "input[data-test-id=email]")
    password_field = form.find_element(By.CSS_SELECTOR, "input[data-test-id=password]")

    email_field.send_keys(username)
    password_field.send_keys(password)
    form.submit()

    wait = WebDriverWait(driver, 10)
    wait.until(lambda driver: "login" not in driver.current_url)

def get_book_id(book_name):
    driver.get(f"https://www.chessable.com/courses/all/created/?search={quote_plus(book_name)}")
    course_link = driver.find_element(By.CSS_SELECTOR, "#books a").get_attribute('href')
    course_id = int([course_link for course_link in course_link.rsplit("/") if course_link][-1])
    return course_id

def new_book(book_name, type = "Opening", color = "White"):
    driver.get("https://www.chessable.com/newcourse/")
    form = driver.find_element(By.CSS_SELECTOR, ".whiteBodyContainer > form[enctype='multipart/form-data']")
    title_field = form.find_element(By.CSS_SELECTOR, "input[name=name]")

    book_type_field = Select(form.find_element(By.CSS_SELECTOR, "select[name=book_type]"))
    piece_type_field = Select(form.find_element(By.CSS_SELECTOR, "select[name=color]"))

    title_field.send_keys(book_name)
    book_type_field.select_by_visible_text(type)
    piece_type_field.select_by_visible_text(color)
    form.submit()

    return get_book_id(book_name)

def create_chapter(name, book_id):
    driver.get(f"https://www.chessable.com/bookadmin.php?bid={book_id}&a=edit&bit=3")
    form = driver.find_element(By.CSS_SELECTOR, ".section_add_a_level form")
    title_field = form.find_element(By.CSS_SELECTOR, "input[name=title]")

    title_field.send_keys(name)
    form.submit()

def import_pgn(games, book_name, chapter):
    driver.get("https://www.chessable.com/import/")
    toggle = driver.find_element(By.CSS_SELECTOR, "#toggleImportMethod")
    toggle.click()
    form = driver.find_element(By.CSS_SELECTOR, "#importForm")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "#submitButton")
    pgn_field = form.find_element(By.CSS_SELECTOR, "#cutAndPastePGN")
    pgn_field.click()

    course_field = Select(form.find_element(By.CSS_SELECTOR, "#bookName"))
    chapter_field = Select(form.find_element(By.CSS_SELECTOR, "#levelDropDown select"))

    pc.copy("\n.".join([str(game) for game in games]))
    pgn_field.send_keys(Keys.CONTROL, 'v')

    course_field.select_by_visible_text(book_name)
    chapter_field.select_by_visible_text(chapter)

    submit_btn.click()

    WebDriverWait(driver, 20).until(lambda driver: driver.find_element(By.CSS_SELECTOR, "#swal2-title").text.startswith("Import "))

def chunks(lst, n):
    res = []
    for i in range(0, len(lst), n):
        res.append(lst[i:i + n])
    return res

def import_course(book_name, filename):
    pgn = open(filename, encoding="utf-8")

    book_id = new_book(book_name)

    data = {}
    while chapter := chess.pgn.read_game(pgn):
        chapter_name = chapter.headers["White"]
        subgames = []
        subgame = chapter
        while subgame and subgame.headers["White"] == chapter_name:
            subgames.append(subgame)
            subgame = chess.pgn.read_game(pgn)

        if len(subgames) > 100:
            # chunk chapter into subchapter
            for i, chunk in enumerate(chunks(subgames, 100), start=1):
                subchapter_name = f"{chapter_name} - Part {i}"
                data[subchapter_name] = chunk
        else:
            data[chapter_name] = subgames

        create_chapter(chapter_name, book_id)

    for chapter, games in data.items():
        print(f"Imported {len(games)} from {chapter}")
        import_pgn(games, book_name, chapter)

load_dotenv()

parser = argparse.ArgumentParser(
                    prog = 'chessable-import',
                    description = 'Imports a course from a PGN into chessable accurately',
                )

parser.add_argument('coursename')
parser.add_argument('filename')

args = parser.parse_args()

pgn_file = args.filename
course_name = args.coursename

if not pathlib.Path(pgn_file).exists():
    die("Must specify a valid pgn file path")

username, password = os.getenv('USERNAME'), os.getenv('PASSWORD')
if not username or not password:
    die("Must configure .env file with credentials")

driver = webdriver.Firefox()

login(username, password)
print(f"Logged in as {username}")
print("Beginning import...")
import_course(course_name, pgn_file)
print("Successfully imported all chapters")

driver.close()
