// Based on algorithm M from "How to Read Floating Point Numbers
// Accurately" by William D Clinger but hardwired to translate from
// base 10 to base 2 with a 53 bit significand.

const max = 2n ** 53n;
const min = 2n ** 52n;

/*
 * f and e are both BigInts specifying the value f * 10^e. For
 * instance 1.05 would be f=105, e=-2.
 */
function algorithmM(f, e) {

  // Find u, v, and k, such that f * 10^e ~= u/v * 2^k and u/v is in
  // the range [min, max). Start by setting u, v, and k such that the
  // equation is trivially satisfied with k = 0 and then adjust u or v
  // until u/v is in the correct range, adjusting k to maintain the
  // equality.

  let u;
  let v;
  let k = 0;

  if (e < 0n) {
    u = f;
    v = 10n ** -e;
  } else {
    u = f * 10n ** e;
    v = 1n;
  }

  while (true) {

    let q = u / v; // BigInt division truncates.

    if (q < min) {
      // q is too small, double the numerator and decrease the
      // exponent to compensate.
      u *= 2n;
      k -= 1n;

    } else if (q >= max) {
      // q is too big, double the denominator and increse the exponent
      // to compensate.
      v *= 2n;
      k += 1n;

    } else {
      // q is in range, so make the float.
      return ratioToFloat(u, v, k);
    }
  }
}

/*
 * Encode the numerator, denominator, and exponent into a "float"
 * rounding the significand to the nearest even value.
 */
function ratioToFloat(u, v, k) {

  let q = u / v;
  let r2 = 2n * (u % v);
  let z = makeFloat(q, k);

  if (r2 < v) {
    // Remainder is less than 1/2, round down.
    return z;

  } else if (r2 > v) {
    // Remainder is greater than 1/2, round up.
    return nextfloat(z);

  } else {
    // Remainder is exactly half.
    if (q % 2n === 0n) {
      // q is already even
      return z;
    } else {
      // q is odd, round to next even.
      return nextfloat(z);
    }
  }
}

/*
 * The next float is the one with a significand one greater than the
 * current. The only trick is when the the significand is already the
 * largest possible adding one wraps around to the smallest possible
 * and we have to adjust the exponent.
 */
function nextfloat(z) {

  let next = z.significand + 1n;

  if (next == max) {
    return makeFloat(min, z.exponent + 1n);
  } else {
    return makeFloat(next, z.exponent)
  }
}

function makeFloat(q, k) {
  return {
    significand: q,
    exponent: k,
  };
}
