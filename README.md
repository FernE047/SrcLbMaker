# SrcLbMaker
A python script to make speedrun.com global leaderboards.

## Installation
You need python 3.6 or higher.

-   First, go to the folder where you want to clone the repository:
    ```sh
    cd yourDirectory
    ```

-   Then clone the repository:
    ```sh
    git clone https://github.com/Rayu1/SrcLbMaker.git
    ```

-   Then install requirements:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
To run the command type `python [filename] [options]`
### Makelb

```
Usage: makelb.py [OPTIONS]

Options:
  -t, --lbtype [wrs|runs|gp|rv|mc]
                                  Type of the leaderboard.

                                  Wrs - world records count,

                                  runs - runs count,

                                  gp - games played count,

                                  rv - runs verified by user,

                                  mc - games moderation count.  [required]
  -L, --lblength INTEGER          Length of the leaderboard.  [default: 100]
```
### Addtodb
```
Usage: addtodb.py [OPTIONS]

Options:
  -n, --nickname TEXT  Runners nickname.
```
## Examples
*   To make a world records count leaderboard run:
    ```sh
    python makelb.py -t wrs -L 50
    ```
*   To add runner "Rayu_" to database run:
    ```sh
    python addtodb.py -n Rayu_
    ```