// Algorithm M from "How to Read Floating Point Numbers Accurately"
// by William D Clinger.

const delta = 10n;
const beta = 2n;
const n = 53n;
const betaN = beta ** n;
const betaNm1 = beta ** (n - 1n);

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
    return makeFloat(betaNm1, z.exporent + 1n);
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