'''
Swagrinth by Mythitorium
'''

import requests
from json import loads
from datetime import datetime
from .project import *
from .user import *
from .errors import *

PATH = "https://api.modrinth.com/v2/"


class Core:
    '''
    Main class for handling, sending, and requesting data
    '''
    def __init__(self, token=""):
        self.token = token

        self.ratelimit = -1
        self.remaining = -1
        self.next_refresh = -1

        self.status = None
    

    def set_auth(self, token):
        self.token = token
    

    def update_ratelimit_info(self, headers):
        self.ratelimit = headers['X-Ratelimit-Limit']
        self.remaining = headers['X-Ratelimit-Remaining']
        self.next_refresh = headers['X-Ratelimit-Reset']
    

    def get_ratelimit(self):
        return {'ratelimit' : self.ratelimit, 'remaining' : self.remaining, 'next_refresh' : self.next_refresh}


    def search(self, query, offset=0, limit=10):
        '''
        Requests a search on modrinth's database

        # DO TO: Implement facets and filters
        '''
        self.validate_args([query, offset, limit],[str, int, int])

        result = requests.get(f"{PATH}search?query={query}&offset={offset}&limit={limit}", headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return SearchResult(loads(result.text))
        else:
            raise NotFound(query, "search")
    

    def get_project(self, project_id: str):
        '''
        Get a project from its id or slug
        '''
        self.validate_args([project_id],[str])

        result = requests.get(f"{PATH}project/{project_id}", headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return Project(loads(result.text))
        else:
            raise NotFound(project_id, "project")


    def get_project_dependencies(self, project_id):
        '''
        '''
        self.validate_args([project_id],[str])
        
        result = requests.get(f"{PATH}project/{project_id}/dependencies", headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            data = loads(result.text)
            return DependencyList(loads(result.text))
        else:
            raise NotFound(project_id, "project")


    def get_project_team(self, project_id):
        '''
        Get a team composition from 
        '''
        self.validate_args([project_id],[str])

        result = requests.get(f"{PATH}project/{project_id}/members", headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return Team(loads(result.text))
        else:
            raise NotFound(project_id, "project")
    

    def get_team(self, team_id):
        self.validate_args([team_id],[str])

        result = requests.get(f"{PATH}project/{team_id}/members", headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return Team(loads(result.text))
        else:
            raise NotFound(team_id, "team")
    

    def get_user(self, user_id):
        self.validate_args([user_id],[str])

        result = requests.get(f"{PATH}user/{user_id}", headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return User(loads(result.text))
        else:
            raise NotFound(user_id, "user")
    

    def get_auth_user(self):
        result = requests.get(f"{PATH}user", headers={'Authorization': self.token})

        if result.status_code == 200:
            return User(loads(result.text))
        elif result.status_code == 401:
            raise NoAccess("No token")
        else:
            raise NotFound('token', "user by")


    def get_user_projects(self, user_id):
        self.validate_args([user_id],[str])

        result = requests.get(f"{PATH}user/{user_id}/projects", headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return [Project(project) for project in loads(result.text)]
        else:
            raise NotFound(user_id, "user")


    def get_project_versions(self, project_id):
        '''
        '''
        self.validate_args([project_id],[str])

        result = requests.get(f"{PATH}project/{project_id}/version", headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return [ProjectVersion(version_dict) for version_dict in loads(result.text)]
        else:
            raise NotFound(project_id, "project")
    

    def get_version(self, version_id):
        '''
        '''
        self.validate_args([version_id],[str])

        result = requests.get(f'{PATH}version/{version_id}', headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return ProjectVersion(loads(result.text))
        else:
            raise NotFound(version_id, "project version")
    

    def get_followed_projects(self):
        result = requests.get(f'{PATH}version/{version_id}', headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return [Projects(project) for project in loads(result.text)]
        elif result.status_code == 401:
            raise NoAccess("No clearance")
        else:
            raise NotFound('token', "user by")
    

    def get_notifs(self):
        result = requests.get(f'{PATH}version/{version_id}', headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return [Notification(notif) for notif in loads(result.text)]
        elif result.status_code == 401:
            raise NoAccess("No clearance")
        else:
            raise NotFound('token', "user by")


    def validate_args(self, args: list, types: list):
        '''
        Used to validate the arguments for functions. Catches bad data before it's used
        '''
        for index in range(len(args)):
            if not type(args[index]) == types[index]:
                raise ArgError(index, type(args[index]), types[index])
