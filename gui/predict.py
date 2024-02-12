import ctypes
import json


def load_predict(so_path: str):
    lib = ctypes.cdll.LoadLibrary(so_path)
    Predict = lib.Predict
    Predict.argtypes = [ctypes.c_char_p]
    Predict.restype = ctypes.c_char_p

    def predict(path: str, pixels: list[float]) -> list[float]:
        data = {"path": path, "pixels": pixels}
        ptr = Predict(json.dumps(data).encode("utf-8"))
        output_s = ctypes.string_at(ptr).decode("utf-8")
        return json.loads(output_s)["prediction"]

    return predict
