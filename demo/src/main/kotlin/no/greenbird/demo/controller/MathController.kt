package no.greenbird.demo.controller

import no.greenbird.demo.service.MathService
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController
import java.math.BigInteger

@RestController
class MathController @Autowired constructor(val mathService: MathService) {

    @GetMapping("/prime")
    fun findNthPrimeNumber(@RequestParam n: Int): BigInteger {
        return mathService.findNthPrimeNumber(n)
    }
}
