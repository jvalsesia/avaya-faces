var ip = location.hostname;

const url_enroll = 'https://' + ip + ':5500/enroll';
const url_schedule = 'https://' + ip + ':5500/recognitionblob';


async function submitEnrollToServer() {

  let userName = document.getElementById("userName").value;
  let canvas = document.getElementById("image_shot");
  //let ctx = canvas.getContext('2d');
  //let image = ctx.getImageData(0, 0, canvas.width, canvas.height);

  //console.log(image);

  let imageBlob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));

  let formData = new FormData();
  console.log(userName);
  formData.append("username", userName);
  formData.append("image", imageBlob, userName + ".png");
  // modify the url accordingly
  let response = await fetch(url_enroll, {
    method: 'POST',
    body: formData
  });

  // convert the response to json, modify it accordingly based on the returned response from your remote server
  let result = await response.json();
  console.log(result);
}



async function submitScheduleToServer() {

  //let userName = document.getElementById("userName").value;
  let canvas = document.getElementById("image_shot");
  //let ctx = canvas.getContext('2d');
  //let image = ctx.getImageData(0, 0, canvas.width, canvas.height);

  //console.log(image);

  let imageBlob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));

  let formData = new FormData();

  //formData.append("username", userName);
  formData.append("image", imageBlob);
  // modify the url accordingly
  let response = await fetch(url_schedule, {
    method: 'POST',
    body: formData
  });

  // convert the response to json, modify it accordingly based on the returned response from your remote server
  let result = await response.json();
  console.log(result);
}