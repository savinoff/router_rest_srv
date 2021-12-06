<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <title></title>
</head>
<body>

    <script language="JavaScript">
     const GetAPI = () => {
       fetch('https://ng.zdsav.keenetic.pro/test/test.json')
       .then((response) => {
         return response.json();
       })
       .then((data) => {
         console.log(data)
         return data;
       });
     }
    </script>

    <div style="background: rgb(191, 191, 209); width: 400px; height: 100px;">
      <p>
        <script language="JavaScript">
          GetAPI()
        </script>
      </p>
    </div>
  </body>
  
  </html>