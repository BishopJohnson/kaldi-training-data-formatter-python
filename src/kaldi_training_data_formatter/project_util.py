import os.path


class ProjectUtil:
    @staticmethod
    def get_song_title(song_id: str) -> str:
        id_elements: list[str] = song_id.split('_')

        if len(id_elements) < 0:
            return ''

        return ' '.join(id_elements[0].split('-'))

    @staticmethod
    def get_user_and_project_id(path: str) -> tuple[str | None, str | None]:
        project_dir: str | None = os.path.dirname(path)
        user_id: str | None = os.path.dirname(os.path.abspath(os.path.join(path, os.path.pardir)))

        if project_dir:
            if user_id:
                return os.path.split(user_id)[1], os.path.split(project_dir)[1]
            else:
                return None, os.path.split(project_dir)[1]
        else:
            return None, None
