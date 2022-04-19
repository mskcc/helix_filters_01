package main
// USAGE:
// updateCaseList cases.txt Sample3,Sample4

import (
    "os"
    "fmt"
    "log"
    "strings"
    "helix/portal"
)

func main() {
    args := os.Args[1:]

    input_filepath := args[0]
    ids_str := args[1]

    ids := strings.Split(ids_str, ",")

    file, err := os.Open(input_filepath)
    if err != nil {
        log.Fatalln("Couldn't open the file", err)
    }
    defer file.Close()

    c := portal.LoadCaseList(file)
    c.AddIds(ids)

    lines := c.ToLines()
    for _, line := range lines {
        fmt.Println(line)
    }
}
