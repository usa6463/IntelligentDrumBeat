package com.example.dslab.firstdesign;

import android.app.Activity;
import android.content.Intent;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.Toast;

public class SecondActivity extends AppCompatActivity {

    final private static String RECORDED_FILE = "/sdcard/VoiceRecorder.mp4";

    MediaPlayer player;
    MediaRecorder recorder;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_second);

        SeekBar seekbar = (SeekBar) findViewById(R.id.seekBar);
        //seekbar.setMax(music.getDuration());

        Button button2 = (Button) findViewById(R.id.button6);
        button2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent();
                intent.putExtra("String", "홈으로");

                setResult(Activity.RESULT_OK, intent);

                finish();
            }
        });

        Button recordBtn = (Button) findViewById(R.id.recordBtn);
        recordBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (recorder != null) {
                    recorder.stop();
                    recorder.release();
                    recorder = null;
                }
                //recorder가 null 아니면 recorder 중지시키고 녹음 시작

                recorder = new MediaRecorder();
                recorder.setAudioSource(MediaRecorder.AudioSource.MIC);
                recorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4);
                recorder.setAudioEncoder(MediaRecorder.AudioEncoder.DEFAULT);
                //마이크의 소리를 녹음하고 , 저장할 파일 포멧을 설정
                recorder.setOutputFile(RECORDED_FILE);

                try {
                    Toast.makeText(getApplicationContext(), "녹음 시작", Toast.LENGTH_LONG).show();

                    recorder.prepare();
                    recorder.start();
                    //녹음 준비 및 시작
                } catch (Exception e) {
                    Log.e("AudioRecorder", "Exception : ", e);
                }
            }
        });

        Button recordStopBtn = (Button) findViewById(R.id.recordStopBtn);
        recordStopBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (recorder == null)
                    return;
                //recorder 가 null 즉, 녹음중인 레코드가 없으면 return
                recorder.stop();
                recorder.release();
                recorder = null;
                //녹음 중이면 정지하고, recorder를 null로 초기화

                Toast.makeText(getApplicationContext(), "녹음 중지", Toast.LENGTH_LONG).show();
            }
        });

        Button button5 = (Button) findViewById(R.id.button5);
        button5.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                Intent intent = new Intent(getApplicationContext(), DesignActivity.class);
                startActivityForResult(intent, 102);
            }

        });

        Button playBtn = (Button) findViewById(R.id.playBtn);
        playBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (player != null) {
                    player.stop();
                    player.release();
                    player = null;
                }
                //player가 null 아니면 정지 한 후, player를 null로 초기화

                Toast.makeText(getApplicationContext(), "녹음 파일 재생", Toast.LENGTH_LONG).show();

                try {
                    player = new MediaPlayer();

                    player.setDataSource(RECORDED_FILE);
                    player.prepare();
                    player.start();

                } catch (Exception ex) {
                    Log.e("AudioRecorder", "Audio play failed ", ex);
                }
            }
        });

        Button playStopBtn = (Button) findViewById(R.id.playStopBtn);
        playStopBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (player == null)
                    return;

                Toast.makeText(getApplicationContext(), "재생 중지",
                        Toast.LENGTH_LONG).show();

                player.stop();
                player.release();
                player = null;
            }
        });
    }
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if(requestCode == 102) {
            //String name = data.getStringExtra("name");
            Toast.makeText(getApplicationContext(), "디자인 레이아웃 " , Toast.LENGTH_LONG).show();
        }

    }
 }


//http://itmir.tistory.com/347
//http://jystudynote.tistory.com/entry/Android간단한녹음예제-AudioRecorder