from dotenv import dotenv_values
import requests
import chess.pgn
from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.select import Select
import pyperclip as pc

config = dotenv_values(".env")
username = config["USERNAME"]
password = config["PASSWORD"]

driver = webdriver.Firefox()

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
    pgn_field = form.find_element(By.CSS_SELECTOR, "#cutAndPastePGN")
    pgn_field.click()

    course_field = Select(form.find_element(By.CSS_SELECTOR, "#bookName"))
    chapter_field = Select(form.find_element(By.CSS_SELECTOR, "#levelDropDown select"))

    pc.copy("\n.".join([str(game) for game in games]))
    pgn_field.send_keys(Keys.CONTROL, 'v')

    course_field.select_by_visible_text(book_name)
    chapter_field.select_by_visible_text(chapter)

    form.submit()

def import_course(book_name, filename):
    pgn = open(filename, encoding="utf-8")

    login(username, password)
    book_id = new_book(book_name)

    data = {}
    while chapter := chess.pgn.read_game(pgn):
        chapter_name = chapter.headers["White"]
        subgames = []
        subgame = chapter
        while subgame and subgame.headers["White"] == chapter_name:
            subgames.append(subgame)
            subgame = chess.pgn.read_game(pgn)
        data[chapter_name] = subgames

        create_chapter(chapter_name, book_id)

    for chapter, games in data.items():
        import_pgn(games, book_name, chapter)

import_course("London System", "game.pgn")
driver.close()
