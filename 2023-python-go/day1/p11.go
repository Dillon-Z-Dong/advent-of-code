package main

import (

	"fmt"
	"io/ioutil"
	"regexp"
	"strconv"
	"strings"

)

func main() {
	data, _ := ioutil.ReadFile("data_day1.txt")
	lines := strings.Split(string(data), "\n")
	//fmt.Println(lines)
	r, _ := regexp.Compile(`(\d)`)	

	sum := 0
	for _, line := range lines {
		matches := r.FindAllString(line, -1) 
		if len(matches) > 0 {
			start := matches[0]
			end := matches[len(matches)-1]
			num, _ := strconv.Atoi(start+end)
			sum += num
		}

	}
	fmt.Println("P1 total sum:", sum)
}