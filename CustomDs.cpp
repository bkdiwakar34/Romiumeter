#include "Arduino.h"
#include "CustomDS.h"

// Buffer class definitions
Buffer::Buffer() {
  _full = false;
  _inx = 0;
  _acc = 0;
  _m = 1.0;
  _c = 0.0;
}

void Buffer::add(float val) {
  // Add data.
  float _val = conval(val);
  _data[_inx & Nmask] = _val;
  if (_full == false) {
    _full = (_inx == 0);
  }
  // Get filtered data
  byte _i = _inx - _nf;
  _acc = _acc + _val - _data[_i & Nmask];
  _dataf[_inx & Nmask] = _acc / _nf;
  _inx++;
}

byte Buffer::inx(void) {
  return _inx & Nmask;
}

bool Buffer::isFull(void) {
  return _full;
}

float Buffer::val(byte pos, bool past) {
  byte _i;
  if (past == true) {
    _i = _inx - pos - (byte) 1;
  } else {
    _i = _inx + pos - (byte) 1;
  }
  return _data[_i & Nmask];
}

float Buffer::valf(byte pos, bool past) {
  byte _i;
  if (past == true) {
    _i = _inx - pos - (byte) 1;
   
  } else {
    _i = _inx + pos - (byte) 1;
   
  }
  return _dataf[_i & Nmask];
}

void Buffer::setconvfac(float m, float c) {
  _m = m;
  _c = c;
}

float Buffer::conval(float val) {
  return  _m * val + _c;
}


// OutDataBuffer class definitions
OutDataBuffer4Float::OutDataBuffer4Float() {
  _sz = 0;
}
void OutDataBuffer4Float::newPacket() {
  _sz = 0;
}
void OutDataBuffer4Float::add(int num) {
   _data[_sz++].num = num;
}
byte OutDataBuffer4Float::sz() {
  return _sz;
}
byte OutDataBuffer4Float::getByte(byte inx) {
byte q = inx / 2;
byte r = inx % 2;
return _data[q].bytes[r];
}
