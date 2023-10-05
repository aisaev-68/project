const { createApp } = Vue;

createApp({
  data() {
    return {
      selectedFile: null,
      uploadStatus: null,
      exportStatus: null,
      versionId: null,
      year: null,
      value_type: null,
      dataChats: [],
    };
  },
  methods: {
    postData(url, payload, config) {
      return axios.post(url, payload, config ? config : {})
        .then(response => {
          return response.data ? response.data : (response.json ? response.json() : null);
        })
        .catch(() => {
          console.warn('Метод ' + url + ' не реализован');
          throw new Error('no "post" method');
        });
    },
    getData(url, payload) {
      return axios.get(url, { params: payload })
        .then(response => {
          return response.data ? response.data : (response.json ? response.json() : null);
        })
        .catch(() => {
          console.warn('Метод ' + url + ' не реализован');
          throw new Error('no "get" method');
        });
    },
    chatData() {
      const params = new URLSearchParams(window.location.search);
      params.set('versionId', this.versionId.toString());
      params.set('year', this.year.toString());
      params.set('value_type', this.value_type.toString());

      this.getData('api/chat_data',
      {
        versionId: this.versionId ? this.versionId : null,
        year: this.year ? this.year : null,
        value_type: this.value_type ? this.value_type : null,
      }
      ).then(({ data }) => {
        this.dataChats = data.items;
        window.history.replaceState(null, null, '?' + params.toString());
      }).catch(() => {
        console.warn('Ошибка при получении данных');
        this.uploadStatus = 'Произошла ошибка при получении данных.';
      });
    },

    uploadFile() {
      const formData = new FormData();
      formData.append('file', this.selectedFile);
      const csrfToken = this.getCookie('csrftoken');

      this.postData('api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-CSRFToken': csrfToken
        }
      })
        .then(response => {
           this.uploadStatus = response.body_message;
        })
        .catch(error => {
            this.uploadStatus = 'Произошла ошибка при загрузке файла.';
            console.warn('Ошибка при загрузке файла', error);
        });
    },

    exportFile() {
      const versionId = parseInt(document.getElementById('versionId').value, 10);

      if (isNaN(versionId)) {
        console.error('Введите корректный идентификатор версии файла.');
        return;
      }

      const csrfToken = this.getCookie('csrftoken');

      const config = {
        responseType: 'text'
      };

      this.getData(`api/export/${versionId}`, null, config)
        .then(response => {
          this.exportStatus = response.body_message;

          // Check if content-disposition header exists
          const contentDispositionHeader = response.headers && response.headers['content-disposition'];

          const fileName = contentDispositionHeader
            ? decodeURIComponent(contentDispositionHeader.split(';')[1].split('filename=')[1].trim())
            : 'file.xlsx';

          // Check if response data exists and is not empty
          if (response.content && response.content.length > 0) {
            const binaryData = atob(response.content);
            const byteArray = new Uint8Array(binaryData.length);
            for (let i = 0; i < binaryData.length; i++) {
              byteArray[i] = binaryData.charCodeAt(i);
            }

            const blob = new Blob([byteArray], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });

            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.setAttribute('download', fileName);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          } else {
            console.error('Данные файла отсутствуют.');
          }
        })
        .catch(error => {
          console.error('Произошла ошибка при отправке запроса:', error);
        });
    },



    getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + '=') {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
     },
    onFileChange(event) {
        this.selectedFile = event.target.files[0];
    },


  }
}).mount('#site');



