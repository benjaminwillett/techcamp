int _trig = 22;
int _echo = 23;
void InitializeUltrasonic(int trig,int echo){
 _trig=trig;
 _echo=echo;
 pinMode(_trig, OUTPUT);
 pinMode(_echo, INPUT);
}

long echo_dist(){
  long time, dist;
  digitalWrite(_trig, LOW);
  delayMicroseconds(2);
  digitalWrite(_trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(_trig, LOW);
  time = pulseIn(_echo, HIGH);
  dist = (time/2) / 29.1;
  return dist;
}

