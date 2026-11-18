import os

pos_tests = [
    "begin skip end",
    "begin X:=1 end",
    "begin X:=1; Y:=2 end",
    "begin while X>0 do X:=X-1 end",
    "begin if X=0 then Y:=1 else Y:=2 end",
    "begin X:=1; while X>0 do X:=X-1 end",
    "begin X:=(A+B)*(C-D) end",
    "begin skip; skip; X:=0 end",
    "begin while 1=1 do skip end",
    "begin if A>B then begin A:=A-B end else begin B:=B-A end end"
]

neg_tests = [
    "begin X:=1", 
    "X:=1 end",
    "begin X:= ; end", 
    "begin while do X:=1 end", 
    "begin if X>0 Y:=1 else Y:=2 end", 
    "begin X:=1 Y:=2 end", 
    "begin 1:=X end", 
    "begin while X>0 do begin X:=X-1 end", 
    "begin X:=Y(*)2 end", 
    "begin if X>0 then X:=1 else end" 
]

def create_tests():
    base_dir = "tests"
    os.makedirs(os.path.join(base_dir, "positive"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "negative"), exist_ok=True)

    for i, code in enumerate(pos_tests, 1):
        with open(os.path.join(base_dir, "positive", f"pos_{i:02d}.sipl"), "w", encoding="utf-8") as f:
            f.write(code + "\n")

    for i, code in enumerate(neg_tests, 1):
        with open(os.path.join(base_dir, "negative", f"neg_{i:02d}.sipl"), "w", encoding="utf-8") as f:
            f.write(code + "\n")
            
    print("Успішно згенеровано 10 позитивних та 10 негативних тестів у папці 'tests'!")

if __name__ == "__main__":
    create_tests()