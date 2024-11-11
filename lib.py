def options() :
    print("-----電影管理系統-----")
    print("1. 匯入電影資料檔")
    print("2. 查詢電影")
    print("3. 新增系統")
    print("4. 修改電影")
    print ("5. 刪除電影")
    print("6. 匯出電影")
    print("7. 離開系統")
    print("-"*24)

    choice = int(input("請選擇操作選項（1-7）："))
    while True:
        try:
            match choice :
                case 1:
                    movie_input()
                case 2:
                    check_movie()
                case 3:
                    add_movie()
                case 4:
                    modify_movie()
                case 5:
                    delete_movie()
                case 6:
                    movie_output()
                case 7:
                    exit()
        except ValueError:
            print("請輸入數字1-7")
            continue

options()

def movie_input():
    pass
def check_movie():
    pass
def add_movie():
    pass
def modify_movie():
    pass
def delete_movie():
    pass
def movie_output():
    pass