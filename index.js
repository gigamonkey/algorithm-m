// Algorithm M from "How to Read Floating Point Numbers Accurately"
// by William D Clinger.

const delta = 10n;
const beta = 2n;
const n = 53n;
const betaN = beta ** n;
const betaNm1 = beta ** (n - 1n);
const max = 2n ** 53n;
const min = 2n ** 52n;


function simpleM(f, e) {

  // Find u, v, and k, such that f * 10^e ~= u/v * 2^k and u/v is in
  // the range [min, max). Start by setting u, v, and k such that the
  // equation is trivially satisfied with k = 0 and then adjust u or v
  // until u/v is in the correct range, adjusting k to maintain the
  // equality.

  let u;
  let v;
  let k = 0n;

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

function algorithmM(f, e) {

  // f * delta ** e == u/v * beta ** k

  if (e < 0n) {
    return loop(f, 10n ** -e);
  } else {
    return loop(f * 10n ** e, 1n);
  }
}

function loop(u, v) {
  let k = 0n;
  while (true) {
    let x = u / v;
    console.log(`u: ${u}; v: ${v}; k: ${k}; x: ${x}`);
    if (betaNm1 <= x && x < betaN) {
      return ratioToFloat(u, v, k);
    } else if (x < betaNm1) {
      u *= beta;
      k -= 1n;
    } else if (betaN <= x) {
      v *= beta;
      k += 1n;
    }
  }
}

function ratioToFloat(u, v, k) {
  let q = u / v;
  let r = u - (q * v);
  let z = makeFloat(q, k);
  if (r < v - r) {
    return z;
  } else if (r > v - r) {
    return nextfloat(z);
  } else if (q % 2n === 0n) {
    return z;
  } else {
    return nextfloat(z);
  }
}

function nextfloat(z) {
  if (z.significand === betaN - 1n) {
    return makeFloat(betaNm1, z.exponent + 1n);
  } else {
    return makeFloat(z.significand + 1n, z.exponent)
  }
}

function makeFloat(q, k) {
  return {
    significand: q,
    exponent: k,
  };
}