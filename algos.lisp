(defun unnormalized-bits (frac)
  "Emit the binary bits of a given fraction. Doesn't normalize."
  (loop with bits = ()
        with v = 0
        for i from 0 to 52
        for next = (+ v (/ (expt 2 i)))
        if (<= next frac)
          do
             (setf v next)
             (push 1 bits)
        else
          do (push 0 bits)
        finally (return (nreverse bits))))

(defun bits (frac)
  "Emit the binary bits of a given fraction normalized. (I.e. first bit is 1.)"
  (loop with bits = ()
        with v = 0
        with emitted = 0
        for i from 0
        for next = (+ v (/ (expt 2 i)))
        if (<= next frac)
          do
             (setf v next)
             (incf emitted)
             (push 1 bits)
        else
          do
             (when (plusp emitted)
               (push 0 bits)
               (incf emitted))
        while (< emitted 53)
        finally (return (nreverse bits))))


(defun bits-to-integer (bits)
  (loop with n = 0 for b in bits do (setf n (+ (* n 2) b)) finally (return n)))

(defun bits-to-rational (bits exp)
  (* (bits-to-integer bits) (expt 2 exp)))


(defun bits-to-string (bits)
  (format nil "~{~a~}" bits))



(defun foo (p)
  (let ((numerator (floor (* 5 (expt 5 -2) (expt 2 p))))
        (denominator (expt 2 (+ 2 p))))
    (values (float (/ numerator denominator) 0d0) numerator denominator)))


(defun encode-float (v)
  (let ((n (numerator v))
        (d (denominator v)))
    (loop for p from 0 to 60
          for num = (round (/ (* n (expt 2 p)) d))
          for f = (float (/ num (expt 2 p)) 0d0)
          do (format t "~&~3d: ~53,'0b ~f " p num f))))


(defun primep (number)
  (when (> number 1)
    (loop for fac from 2 to (isqrt number) never (zerop (mod number fac)))))

(defun next-prime (number)
  (loop for n from number when (primep n) return n))


(defun factors (n)
  (when (> n 1)
    (if (primep n)
      (cons n nil)
      (let ((f (first-prime-factor n 2)))
        (cons f (factors (/ n f)))))))

(defun first-prime-factor (n f)
  (if (zerop (mod n f))
    f
    (first-prime-factor n (next-prime (1+ f)))))
