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

print("Menu\n1. for repo link\n2. local path")


while(1):
    choice = (input("Enter your choice: ")).strip()
    link_path = (input("Enter the link or local path: ")).strip()

    if(choice == "1"):
        repo = SetUpRepo(link=link_path,path=None)

    elif choice == "2":
        repo = SetUpRepo(link=None,path=link_path)
    else:
        print("Wrong choice enter again")
        continue

    if repo == "reload_and_continue":
        continue
    else:
        print("repo initialised Successfully!!")
        break


