package com.jarvis.jarvisimagedrop;

import android.app.ProgressDialog;
import android.content.Context;
import android.net.Uri;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.annotations.DeferredApi;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class UploadImage_ {
    private Context context;
    private ProgressDialog progressDialog;
    private Uri imageUri;
    private TextView urlShowTV;

    public UploadImage_(Context context, Uri imageUri, TextView urlShowTV) {
        this.context = context;
        this.imageUri = imageUri;
        this.urlShowTV = urlShowTV;
    }

    public void uploadImage(UploadCallback callback) {
        progressDialog = new ProgressDialog(context);
        progressDialog.setTitle("Uploading file...");
        progressDialog.show();

        SimpleDateFormat formatter = new SimpleDateFormat("yyyy_MM_dd_HH_mm_ss", Locale.CANADA);
        Date now = new Date();
        String filename = formatter.format(now);

        StorageReference storageReference = FirebaseStorage.getInstance().getReference("images/" + filename);
        storageReference.putFile(imageUri)
                .addOnSuccessListener(taskSnapshot -> {
                    // Image uploaded successfully, get the download URL
                    storageReference.getDownloadUrl().addOnSuccessListener(uri -> {
                        // Get the download URL and pass it to the callback
                        String downloadUrl = uri.toString();
                        callback.onSuccess(downloadUrl);
                        // Here you can use the download URL to display the image, share it, etc.
                        Toast.makeText(context, "Image uploaded successfully. Download URL: " + downloadUrl, Toast.LENGTH_SHORT).show();
                    });
                    if (progressDialog.isShowing())
                        progressDialog.dismiss();
                }).addOnFailureListener(e -> {
                    if (progressDialog.isShowing())
                        progressDialog.dismiss();
                    callback.onFailure("Failed to upload image: " + e.getMessage());
                });
    }

    public interface UploadCallback {
        void onSuccess(String downloadUrl);
        void onFailure(String errorMessage);
    }

}
