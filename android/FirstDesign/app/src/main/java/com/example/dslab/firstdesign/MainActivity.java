package com.example.dslab.firstdesign;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button button = (Button) findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                Intent intent = new Intent(getApplicationContext(), SecondActivity.class);
                startActivityForResult(intent, 101);
            }
        });

        ImageView imageView= (ImageView) findViewById(R.id.imageView);
        imageView.setImageResource(R.drawable.record);

    }

    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if(requestCode == 101) {
            String name = data.getStringExtra("name");
            Toast.makeText(getApplicationContext(), "홈으로 돌아갑니다. " , Toast.LENGTH_LONG).show();
        }

    }
}
