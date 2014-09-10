      var ytState;

      function onPlayerStateChange(newState) {
      	ytplayer = document.getElementById("ytPlayer");    
      	ytState=newState;
      	if (ytState==5) 
      	{
      	ytplayer.playVideo();
      	}
      	else if (ytState==0)
      	{
      	cueNextSong();
      	}
      }
      
      function Play()
      {
      ytplayer = document.getElementById("ytPlayer");
      ytplayer.playVideo();
      }
      
      
      
      function Pause()
      {
      ytplayer = document.getElementById("ytPlayer");
      ytplayer.pauseVideo();
      }
      
      
      
      function reloadSongs()
      {
        counter = -1;
        $.ajax({
        url: 'getsongids',
        success: onReloadSongs,
        dataType: 'json'});
      }
      
      function onReloadSongs(data)
      {
      videoids = data;
      nSongs = data.length;
      cueNextSong();
      }
      
      function cueNextSong()
      {
      counter++;
      if (counter == nSongs)
      {
      reloadSongs();
      return;
      }
      ytplayer = document.getElementById("ytPlayer");
      var songid = videoids[counter];
      ytplayer.cueVideoById(songid);
      }
      

      function onYouTubePlayerReady(playerId) {
            ytplayer = document.getElementById("ytPlayer");    
            ytplayer.addEventListener("onStateChange", "onPlayerStateChange");
            reloadSongs();
     }            
      
      function InitVideoPlayer() {
      
      	var params = { allowScriptAccess: "always" };
     	var atts = { id: "ytPlayer" };
      	swfobject.embedSWF("http://www.youtube.com/apiplayer?" +
      	            "&enablejsapi=1&playerapiid=mojplayer", 
                           "videoBox", "480", "310", "8", null, null, params, atts);
      }
      
      
      var videoids;
      var counter;
      var nSongs;
      $().ready(InitVideoPlayer);