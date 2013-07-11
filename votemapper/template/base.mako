<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<% import json %>
<html>
<head>
    <meta http-equiv='Content-Type' content='Type=text/html; charset=utf-8'>
    <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.4.4/leaflet.css" />
    <!--[if lte IE 8]><link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.4.4/leaflet.ie.css" /><![endif]-->
    <style type="text/css">
        .info {
            padding: 6px 8px;
            font: 14px/16px Arial, Helvetica, sans-serif;
            background: white;
            background: rgba(255, 255, 255, 0.8);
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
            border-radius: 5px;
            width: 300px;
        }
        .info h4 {
            margin: 0 0 5px;
            color: #777;
        }

        td.persent, td.count { text-align: right; }
        td.persent:after { content: "%"; }

    </style>

    <script type="text/javascript">
        var participants = ${ dict([(p.id, p.as_dict()) for p in env.participants]) | json.dumps, n };
        var levels = ${ dict([(l.id, l.as_dict()) for l in env.levels]) | json.dumps, n };

        var currentLevel;
    </script>


    

</head>
<body>
    <div id="map" style="position: absolute; left: 0px; top: 0px; right: 0px; height: 100%; "></div>

    <div id="info" class="info">
        <h4 id="result-head">Общие итоги голосования</h4>
        <table style="width: 100%;">
            %for p in env.participants:
            <tr>
                <td style="background-color: #${p.color | n}; width: 16px;">&nbsp;</td>
                <td>
                    <a href="#" onClick="setStyle('participant', ${p.id}); return false;">
                    ${p.name}
                    </a>
                </td>
                <td id="p-${p.id}-p" class="persent">&nbsp;</td>
                <td id="p-${p.id}-c" class="count">&nbsp;</td>
            </tr>
            %endfor

            <tr>
                <td colspan="4"></td>
            </tr>

            <tr>
                <td colspan="2">
                    <a href="#" onClick="setStyle('turnout'); return false;">
                        Явка
                    </a>
                </td>
                <td id="turnout-p" class="persent">&nbsp;</td>
                <td id="turnout-c" class="count">&nbsp;</td>
            </tr>

            <tr>
                <td colspan="2">
                    <a href="#" onClick="setStyle('absentee'); return false;">
                        Открепительные
                    </a>
                </td>
                <td id="absentee-p" class="persent">&nbsp;</td>
                <td id="absentee-c" class="count">&nbsp;</td>
            </tr>

            <tr>
                <td colspan="4"></td>
            </tr>

            <tr>
                <td colspan="4">
                    Итоговое место:
                    <a href="#" onClick="setStyle('place', 1); return false;">1-е</a> | 
                    <a href="#" onClick="setStyle('place', 2); return false;">2-е</a> |
                    <a href="#" onClick="setStyle('place', 3); return false;">3-е</a>
                </td>
            </tr>
        </table>

    </div>

    <div id="legend" class="info">
        <h4 id="style-title"></h4>

        <table style="width: 100%;">
            <tr id="style-color"></tr>
            <tr id="style-value"></tr> 
        </table>

    </div>

    <script src="http://cdn.leafletjs.com/leaflet-0.4.4/leaflet.js"></script>
    <script src="${static_url}/js/map.js"></script>


    <script type="text/javascript">

        var parameterStat = ${ env.parameter_stat() | json.dumps, n}
        var participantVoteStat = ${ env.participant_vote_stat() | json.dumps, n };
        
        // текущий способ раскраски полигонов и участник выборов
        var currentStyle = 'participant';
        var currentStyleP = 1;
        var currentStyleBase;

        L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: 'Map data © OpenStreetMap contributors',
            opacity: 0.6
        }).addTo(map);

    </script>


    %for level in env.levels:
        <script type="text/javascript" src="level-${level.id}.js"></script>
    %endfor

    <script type="text/javascript">
        setStyle('turnout');
        switchLevel(levels[1]);
    </script>

</body>
</html>