gpus = [
    {
        "gpu": "3080",
        "suffix": "&fv_gpu.chip=NVIDIA%20RTX%203080",
        "price": 0,
        "prevprice": 0,
        "target": 850
    },
    {
        "gpu": "6800xt",
        "suffix": "&fv_gpu.chip=AMD%20RX%206800%20XT",
        "price": 0,
        "prevprice": 0,
        "target": 850
    }
]

# for gpu in gpus:
#     link = 'https://www.gputracker.eu/nl/search/category/1/grafische-kaarten?onlyInStock=true'+gpu["suffix"]
#     print(link)

test = "a and b and c"
q = test.replace(" ", "%20")
print(q)