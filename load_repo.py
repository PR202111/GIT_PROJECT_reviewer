from typing import Optional,Union
from git import Repo
from CONFIG import REPO_PATH
def SetUpRepo(link:Optional[str] = None,path:Optional[str] = None) -> Union[str,Repo]:
    if link is not None:
        try:
            print("Cloning...")
            repo = Repo.clone_from(link,REPO_PATH)
            return repo
        except Exception as e:
            print(f"{e}: Wrong repo link provided")
            return "reload_and_continue"
    elif path is not None:
        try:
            print("Cloning...")
            repo = Repo(path)
            return repo
        except Exception as e:
            print(f"{e}: wrong path provided")
            return "reload_and_continue"
    else:
        print("No repo link or path was given")
        return "reload_and_continue"
    

if __name__ == "__main__":
    while True:
        link_path = input("Enter Repo link: ")
        repo = SetUpRepo(link_path)
        if repo == "reload_and_continue":
            continue
        else: break
    







