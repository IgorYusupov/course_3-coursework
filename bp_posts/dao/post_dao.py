import json
from json import JSONDecodeError
from exceptions.data_exceptions import DataSourceError
from post import Post


class PostDAO:
    """
    Менеджер постов - загружает, ищет, вытаскивает по pk и пользователю
    """
    def __init__(self, path):
        self.path = path

    def _load_data(self):
        """
        Загружает данные из JSON и возвращает список словарей
        """
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                posts_data = json.load(file)
        except(FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f"Не удаётся получить данные из файла {self.path}")

        return posts_data

    def _load_posts(self):
        """
        Возвращает список экземпляров Post
        """
        posts_data = self._load_data()
        list_of_posts = [Post(**post_data) for post_data in posts_data]

        return list_of_posts

    def get_posts_all(self):
        """
        Получает все посты, возвращает список экземпляров класса Post
        """
        posts = self._load_posts()

        return posts

    def get_by_pk(self, pk):
        """
        Возвращает один пост по его идентификатору
        """
        if type(pk) != int:
            raise TypeError("pk must be an int")

        posts = self._load_posts()
        for post in posts:
            if post.pk == pk:

                return post

    def search_in_content(self, substring):
        """
        Возвращает список постов по ключевому слову
        """
        if type(substring) != str:
            raise TypeError("substring must be an str")

        substring = substring.lower()
        posts = self._load_posts()

        matching_posts = [post for post in posts if substring in post.content.lower()]

        return matching_posts

    def get_by_poster(self, user_name):
        """
        Возвращает посты определённого автора
        """
        if type(user_name) != str:
            raise TypeError("user_name must be an str")

        user_name = user_name.lower()
        posts = self._load_posts()

        matching_posts = [post for post in posts if user_name in post.content.lower()]

        return matching_posts
