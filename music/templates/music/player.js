		{% if playlist_songs %}
			<script type="text/javascript">
			//<![CDATA[
				$(document).ready(function(){
					var myPlaylist = new jPlayerPlaylist({
					jPlayer: "#jquery_jplayer_N",
					cssSelectorAncestor: "#jp_container_N"
				},[
                        {% for ps in playlist_songs %}
				{% autoescape off %}
				{
					title:"{{ps.full_name}} - {{ps.song_name}}",
					mp3:"/media/{{ps.file_path|urlencode}}",
					{% if ps.cover_url %}
					poster:"/media/cover_art/{{ps.cover_url}}"
					{% endif %}
				},
				{% endautoescape %}
			{% endfor %}
				], {
					playlistOptions: {
						enableRemoveControls: true
					},
					swfPath: "/static/music/assets/js",
					supplied: "mp3, mp4, ebmv, ogv, m4v, oga",
					useStateClassSkin: true,
					autoBlur: false,
					smoothPlayBar: true,
					keyEnabled: true,
					remainingDuration: true,
					toggleDuration: true
				});
			});
			//]]>
			</script>
		{% endif %}

