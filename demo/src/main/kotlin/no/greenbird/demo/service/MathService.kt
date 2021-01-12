package no.greenbird.demo.service

import org.springframework.stereotype.Service
import java.math.BigInteger
import java.util.stream.Collectors
import java.util.stream.Stream


@Service
class MathService {


    fun findNthPrimeNumber(n: Int): BigInteger {
        return Stream.iterate(BigInteger.valueOf(2)) { obj: BigInteger -> obj.nextProbablePrime() }
            .limit(n.toLong())
            .collect(Collectors.toList())
            .last()
    }
}

