import os.path
from typing import Tuple


class ProjectUtil:
    @staticmethod
    def get_user_and_project_id(path: str) -> Tuple[str | None, str | None]:
        project_dir: str | None = os.path.dirname(path)
        user_id: str | None = os.path.dirname(os.path.abspath(os.path.join(path, os.path.pardir)))

        if project_dir:
            if user_id:
                return os.path.split(user_id)[1], os.path.split(project_dir)[1]
            else:
                return None, os.path.split(project_dir)[1]
        else:
            return None, None
