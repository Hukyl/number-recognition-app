package main

import "C"
import (
	"encoding/json"
	"log"

	"github.com/Hukyl/mlgo/matrix"
	"github.com/Hukyl/mlgo/nn"
)

func loadJSON(input_c *C.char) map[string]interface{} {
	documentString := C.GoString(input_c)
	var input map[string]interface{}
	err := json.Unmarshal([]byte(documentString), &input)
	if err != nil {
		log.Fatal(err)
	}
	return input
}

func dumpJSON(output map[string]interface{}) *C.char {
	outputB, err := json.Marshal(output)
	if err != nil {
		log.Fatal(err)
	}
	return C.CString(string(outputB))
}

/*****************************************************/

//export Predict
func Predict(input_c *C.char) *C.char {
	input := loadJSON(input_c)

	pixelsI, ok := input["pixels"].([]interface{})
	if !ok {
		log.Fatal("invalid pixels")
	}

	pixels := make([]float64, len(pixelsI))
	for i := range pixelsI {
		pixels[i] = pixelsI[i].(float64)
	}

	path, ok := input["path"].(string)
	if !ok {
		log.Fatal("invalid path")
	}

	pixelMatrix, _ := matrix.NewMatrix([][]float64{pixels})

	model, err := nn.LoadNeuralNetwork(path)
	if err != nil {
		log.Fatal(err)
	}
	predictionMatrix := model.Predict(pixelMatrix.T())

	prediction := make([]float64, predictionMatrix.RowCount())
	for i := 0; i < predictionMatrix.RowCount(); i++ {
		prediction[i], _ = predictionMatrix.At(i, 0)
	}

	output := make(map[string]interface{})
	output["prediction"] = prediction

	return dumpJSON(output)
}

func main() {}
