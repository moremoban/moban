Fork [moban](https://github.com/moremoban/moban) by clicking "Fork".

## Using virtualenv and Remote Configuration
1. `pip3 install virtualenv`
2. Move to the location where you want to setup moban and type `mkdir moban` in the terminal
3. `cd moban`
3. Type `virtualenv venv`
4. `source venv/bin/activate`
5. `git clone git clone https://github.com/YOUR_USERNAME/moban.git`
6. `cd moban`
7. `pip3 install -e .`
7. `git remote add origin https://github.com/YOUR_USERNAME/moban.git`
8. `git remote add upstream https://github.com/moremoban/moban.git`

When you want to update your local copy type <br> `git fetch upstream` <br> `git merge upstream/master` <br> `git push`

Steps for creating a Pull Request
1. Checkout to the develop branch `git checkout develop`
3. Start a new branch with a suitable name `git checkout -b branch_name`
4. Develop a new feature or solve an existing issue 
5. Add the changed files `git add file_name`
6. Commit with a suitable message `git commit -m " Changes made "`
7. Push `git push origin branch_name`
8. Go to the Github Repository and create a pull request to the develop branch

