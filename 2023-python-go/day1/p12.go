package main

import (
    "fmt"
    "io/ioutil"
    "regexp"
    "strconv"
    "strings"
)

func main() {
    data, err := ioutil.ReadFile("data_day1.txt")
    if err != nil {
        fmt.Println("Error reading file:", err)
        return
    }
    
    // Single regex pattern for both digits and number words
    r := regexp.MustCompile(`one|two|three|four|five|six|seven|eight|nine|\d`)
    
    numberMap := map[string]string{
        "one": "1", "two": "2", "three": "3", "four": "4", 
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
    }
    
    sum := 0
    for _, line := range strings.Split(string(data), "\n") {
        var matches [] string
        // Search starting from each position
        for i := 0; i < len(line); i++ {
            if match := r.FindString(line[i:]); match != "" {
                if num, exists := numberMap[match]; exists {
                    matches = append(matches, num)
                } else {
                    matches = append(matches, match)
                }
            }
        }
        
        if len(matches) > 0 {
            num, _ := strconv.Atoi(matches[0] + matches[len(matches)-1])
            sum += num
        }
    }
    fmt.Println("P2 sum:", sum)
}