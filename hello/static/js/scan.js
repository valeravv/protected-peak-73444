
function unrz(r,u) {
    return (r + 100).toString().substring(1) + (u + 10000000000000).toString().substring(1)
}

ri = 0; u = 1289034;
regs = [77,78,24,66,61,02,16,72,74,52,63,05,24,26,54,42,59,14,65,28]

r = regs[ri]

function next_r() {
  ri = ri + 1;
  r = regs[ri];
  if (ri >= regs.length) {
    next_n()
  } else {
    plan()
  }
}

function next_n() {
  ri = 0;
  r = regs[ri];
  u = u + 1;
  plan()
}

next_n_fn = next_n
next_r_fn = next_r

function plan() {
if (planned) setTimeout(function () {
  fetch(window.location.origin+'/unrz/'+unrz(r,u))
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    console.log(data);
    next_n_fn()
  })
  .catch(function (err) {
    next_r_fn()
  }); 
},600)
}

planned = true

