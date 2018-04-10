//Per State Unemployment from
//https://github.com/floswald/Rdata/

var data = {};
var surpriseData = {};
var minYear = 1981;
var maxYear = 1998;

var curYear = minYear;


//US States GeoJSON
var map;

var mapWidth = 500;
var mapHeight = 300;

var smallMapW = 200;
var smallMapH = 100;

var projection = d3.geo.albersUsa()
      .scale(500)
      .translate([mapWidth/2,mapHeight/2]);

var smallProj = d3.geo.albersUsa()
  .scale(200)
  .translate([smallMapW/2,smallMapH/2]);

var path = d3.geo.path().projection(projection);

var smallPath = d3.geo.path().projection(smallProj);

var rate = d3.scale.quantile()
    .domain([0,12])
    .range(colorbrewer.RdPu[9]);

var surprise = d3.scale.quantile()
    .domain([-.15,.15])
    .range(colorbrewer.RdBu[11].reverse());

var diff = d3.scale.quantile()
  .domain([-12,12])
  .range(colorbrewer.RdYlBu[9].reverse());

var belief = d3.scale.quantile()
.domain([-1,1])
.range(colorbrewer.RdYlBu[9]);

var y = d3.scale.linear()
  .domain([0,1])
  .range([0,smallMapH]);

var x = d3.scale.linear()
  .domain([0,maxYear-minYear])
  .range([0,smallMapW]);


//1991 was a boom year
var boomYear = 1998 - minYear;

//1981 was a bust year
var bustYear = 1981 - minYear;

//assume no geographic pattern
var uniform = {};

//assume things will be like our boom year
var boom = {};

//asume things will be like our bust year
var bust = {};

var max_street = {};
var min_street = {};

d3.csv("http://localhost:8000/street_scores.csv", function(row){
   if(row.street.length > 0){
	   var rates = [];
	   var current_max = 0;
	   var current_min = 1000;
	   for(var i = 1; i<=20; i++){
	     var current_value = row["num"+i.toString()];
	     if (current_value > current_max){
		current_max = current_value;
	     }else if (current_value < current_min){
		current_min = current_value;
	     }
	     rates.push(+row["num"+i.toString()]);
	   }
	   max_street[row.street] = current_max;
	   min_street[row.street] = current_min;

	   data[row.street] = rates;
   }
   return;
  },
  function(done){
       d3.json("http://localhost:8000/states.json", function(d){
               map = d;
               makeMaps();
       });
       
  }
);

function makeMaps(){
  
  calcSurprise();
  console.log(surpriseData);
  var text = "";
  for (key in surpriseData){ 
	text = text + (key+"," + surpriseData[key]+"\n"); 
  }
  document.getElementById("surpriseData").textContent = text;

  var text_uni = "";
  for (key in uniformData){ 
	text_uni = text_uni + (key+"," + uniformData[key]+"\n"); 
  }
  document.getElementById("uniformData").textContent = text_uni;

  var text_base = "";
  for (key in baseData){ 
	text_base = text_base + (key+"," + baseData[key]+"\n"); 
  } 
  document.getElementById("baseData").textContent = text_base;

  var text_uni_conf = "";
  for (value in uniform.pM){ 
	text_uni_conf = text_uni_conf + (uniform.pM[value]+"\n"); 
  }
  document.getElementById("uniformconf").textContent = text_uni_conf;

  var text_base_conf = "";
  for (value in boom.pM){ 
	text_base_conf = text_base_conf + (boom.pM[value]+"\n"); 
  }
  document.getElementById("baseconf").textContent = text_base_conf;

  var text_norm_conf = "";
  for (value in bust.pM){ 
	text_base_conf = text_base_conf + (bust.pM[value]+"\n"); 
  }
  document.getElementById("normconf").textContent = text_base_conf;




  //Make both our density and surprise maps
  //makeBigMap(rate,data,"Unemployment","rates");
  //makeBigMap(surprise,surpriseData,"Surprise","surprise");
  
  //makeSmallMap("uniformE",d3.select("#uniform"));
  //makeSmallMap("uniformEO",d3.select("#uniform"));
  //makeAreaChart(uniform.pM,"uniformB",d3.select("#uniform"));
  
  //makeSmallMap("boomE",d3.select("#boom"));
  //makeSmallMap("boomEO",d3.select("#boom"));
  //makeAreaChart(boom.pM,"boomB",d3.select("#boom"));
  
  //makeSmallMap("bustE",d3.select("#bust"));
  //makeSmallMap("bustEO",d3.select("#bust"));
  //makeAreaChart(bust.pM,"bustB",d3.select("#bust"));
  
  //update();
}

function makeSmallMap(id,parent){
  var smallMap = parent.append("svg").attr("id",id);
  smallMap.selectAll("path")
    .data(map.features)
    .enter()
    .append("path")
    .attr("d",smallPath)
    .attr("fill","#333");
  
}

function makeAreaChart(data,id,parent){
  var areaChart = parent.append("svg").attr("id",id);
  
  areaChart.selectAll("rect")
    .data(data)
    .enter()
    .append("rect")
    .attr("x",function(d,i){ return x(i);})
    .attr("y",function(d){ return smallMapH-y(d);})
    .attr("width",x(1)-x(0))
    .attr("height",function(d){ return y(d);})
    .attr("fill",function(d,i){ return belief(d); });
}

function makeBigMap(theScale,theData,theTitle,id){
  //Make a "big" map. Also merges given data with our map data
  var mainMap = d3.select("#main").append("svg")
  .attr("id",id).attr("height",mapHeight);
  
  mainMap.append("g").selectAll("path")
  .data(map.features)
  .enter()
  .append("path")
  .datum(function(d){ d[id] = theData[d.properties.NAME]; return d;})
  .attr("d",path)
  .attr("fill","#333")
  .append("svg:title")
  .text(function(d){ return d.properties.NAME; });
  
  var scale = mainMap.append("g");
  
  scale.append("text")
  .attr("x",mapWidth/2)
  .attr("y",15)
  .attr("font-family","Futura")
  .attr("text-anchor","middle")
  .attr("font-size",12)
  .text(theTitle);
  
  var legend = scale.selectAll("rect")
  .data(theScale.range())
  .enter();
  
  legend.append("rect")
  .attr("stroke","#fff")
  .attr("fill",function(d){ return d;})
  .attr("y",35)
  .attr("x",function(d,i){ return mapWidth/2 - (45) + 10*i; })
  .attr("width",10)
  .attr("height",10)
  
  legend.append("text")
  .attr("x",function(d,i){ return mapWidth/2 - (40) + 10*i; })
  .attr("y",30)
  .attr("font-family","Futura")
  .attr("text-anchor","middle")
  .attr("font-size",8)
  .text(function(d,i){
        var label = "";
        if(i==0){
          label = d3.format(".2n")(theScale.invertExtent(d)[0]);
        }
        else if(i==theScale.range().length-1){
   
          label = d3.format(".2n")(theScale.invertExtent(d)[1]);
        }
        return label;
  });
 
   mainMap.selectAll("path")
   .attr("fill",function(d){ return theScale(d[id][curYear-minYear]);});
}

function update(){
  //Update our big maps, our difference maps, and model maps.
  curYear = +d3.select("#year").node().value;
  
  d3.select("#yearLabel").text(curYear);
  
  d3.select("#rates").selectAll("path")
  .attr("fill",function(d){ return rate(d.rates[curYear-minYear]);});
  
  d3.select("#surprise").selectAll("path")
  .attr("fill",function(d){ return surprise(d.surprise[curYear-minYear]);});
  
  var avg = average();
  d3.select("#uniformE").selectAll("path")
  .attr("fill",rate(avg));
  
  d3.select("#uniformEO").selectAll("path")
  .attr("fill",function(d){ return diff( d.rates[curYear-minYear]-avg);});
  
  d3.select("#boomE").selectAll("path")
  .attr("fill",function(d){ return rate(d.rates[boomYear]);});
  
  d3.select("#boomEO").selectAll("path")
  .attr("fill",function(d){ return diff(d.rates[curYear-minYear]-d.rates[boomYear]);});
  
  d3.select("#bustE").selectAll("path")
  .attr("fill",function(d){ return rate(d.rates[bustYear]);});
  
  d3.select("#bustEO").selectAll("path")
  .attr("fill",function(d){ return diff(d.rates[curYear-minYear]-d.rates[bustYear]);});
  
  d3.select("#uniformB").selectAll("rect")
  .attr("fill-opacity",function(d,i){ return i==(curYear-minYear)? 1 : 0.3;});
  
  d3.select("#boomB").selectAll("rect")
  .attr("fill-opacity",function(d,i){ return i==(curYear-minYear)? 1 : 0.3;});
  
  d3.select("#bustB").selectAll("rect")
  .attr("fill-opacity",function(d,i){ return i==(curYear-minYear)? 1 : 0.3;});
}

function average_num(prop, i){
  //Average scores for current street point.
  var sum = 0;
  var n = 0;

  var int_part = parseInt(i/4);

  for(var i = int_part * 4; i < (int_part+1) * 4; i++){
	    sum+= data[prop][i];
	    n++;
  }
  return sum/n;
}

function median(numbers) {
    // median of [3, 5, 4, 4, 1, 1, 2, 3] = 3
    var median = 0, numsLen = numbers.length;
    numbers.sort();
 
    if (
        numsLen % 2 === 0 // is even
    ) {
        // average of two middle numbers
        median = (numbers[numsLen / 2 - 1] + numbers[numsLen / 2]) / 2;
    } else { // is odd
        // middle number only
        median = numbers[(numsLen - 1) / 2];
    }
 
    return median;
}

function median_num(prop, i){
  //Median score for current street point.
  current_values = [];

  var int_part = parseInt(i/4);

  for(var i = int_part * 4; i < (int_part+1) * 4; i++){
	current_values = current_values.concat(data[prop][i]);
  }
  return median(current_values);
}

function average_street(prop){
  //Average scores for current street.
  //var index = i ? i : curYear-minYear;
  var sum = 0;
  var n = 0;
  for(var i = 0; i < 20; i++){
	    sum+= data[prop][i];
	    n++;
  }
  return sum/n;
}

function sumU_num(prop, i){
  //Sum scores for current street.
  //var index = i ? i : curYear-minYear;
  var sum = 0;
  var int_part = parseInt(i/4);

  for(var i = int_part * 4; i < (int_part+1) * 4; i++){
	    sum+= data[prop][i];
  }
  return sum;
}

function sumU_street(prop){
  //Sum scores for current street.
  //var index = i ? i : curYear-minYear;
  var sum = 0;
  for(var i = 0; i < 20; i++){
	    sum+= data[prop][i];
  }
  return sum;
}

function KL(pmd,pm){
  return pmd * (Math.log ( pmd / pm   )/Math.log(2));
}

function maxSurprise(){
  var curM = 0;
  var sMax;
  for(var prop in surpriseData){
    sMax = Math.max.apply(null, surpriseData[prop]);
    curM = sMax>curM ? sMax : curM;
  }
  return curM;
}

function makeRandom(){
  //Random fake data in [-1,1]
  var randData = {};
  for(var prop in data){
    randData[prop] = [];
    for(var i = 0;i<=maxYear-minYear;i++){
      randData[prop][i] = Math.random()>0.5 ? -1*Math.random() : Math.random();
    }
  }
  return randData;
}

window.temp = {
    spareNormal: undefined
};

Math.normal = function (mean, standardDeviation) {
    let q, u, v, p;

    mean = mean || 0.5;
    standardDeviation = standardDeviation || 0.125;

    if (typeof temp.spareNormal !== 'undefined') {
        v = mean + standardDeviation * temp.spareNormal;
        temp.spareNormal = undefined;

        return v;
    }

    do  {
        u = 2.0 * Math.random() - 1.0;
        v = 2.0 * Math.random() - 1.0;

        q = u * u + v * v;
    } while (q >= 1.0 || q === 0);

    p = Math.sqrt(-2.0 * Math.log(q) / q);

    temp.spareNormal = v * p;
    return mean + standardDeviation * u * p;
}

function calcSurprise(){

  
  for(var prop in data){
    surpriseData[prop] = [];
    uniformData[prop] = [];
    baseData[prop] = [];
    for(var i = 0; i < 20; i++){
      surpriseData[prop][i] = 0;
      uniformData[prop][i] = 0;
      baseData[prop][i] = 0;
    }
  }
  // Start with equiprobably P(M)s
  // For each year:
  // Calculate observed-expected
  // Estimate P(D|M)
  // Estimate P(M|D)
  // Surprise is D_KL ( P(M|D) || P(M) )
  // Normalize so sum P(M)s = 1
  
  //0 = uniform, 1 = boom, 2 = bust
  
  //Initially, everything is equiprobable.
  var pMs =[(1/3),(1/3),(1/3)];

  uniform.surprise = [];
  boom.surprise = [];
  //bust.surprise = [];
  
  uniform.pM = [pMs[0]];
  boom.pM = [pMs[1]];//Max of street
  bust.pM = [pMs[2]];//Min of street
  
  var pDMs = [];
  var pMDs = [];
  var avg;
  var total;

  var normal_fit = {"all" : [4.68088452, 0.62863384], "R._Cristina_Procópio_Silva" : [4.92394878, 0.62351231], "R._Maciel_Pinheiro" : [4.84016850, 0.28028584], "R._Inácio_Marquês_da_Silva": [4.84231882, 0.46291311], "R._Manoel_Pereira_de_Araújo": [3.65700904, 0.19215810], "Av._Mal._Floriano_Peixoto": [ 5.04950088, 0.34203741], "R._Edésio_Silva": [4.77236112, 0.48215430]};
  
  //Bayesian surprise is the KL divergence from prior to posterior
  var kl;
  var diffs = [0,0,0];
  var sumDiffs = [0,0,0];
  for(var i = 0; i < 20; i++){
    sumDiffs = [0,0,0];

    //Calculate per state surprise
    for(var prop in data){

      var norm_data = normal_fit[prop]
      var norm_estimate = Math.normal(norm_data[0], norm_data[1]);

      avg_street  = average_street(prop);//For whole street
      total_street = sumU_street(prop);
      avg_num = average_num(prop, i);//median_num(prop, i);//For current point
      total_num = sumU_num(prop, i);
      
      //Estimate P(D|M) as 1 - |O - E|
      //uniform
      diffs[0] = ((data[prop][i]/total_street) - (avg_street/total_street));
      pDMs[0] = 1 - Math.abs(diffs[0]);
      //Average per num
      diffs[1] = ((data[prop][i]/total_street) - (avg_num/total_street));
      pDMs[1] = 1 - Math.abs(diffs[1]);
      //normal
      diffs[2] = ((data[prop][i]/total_street) - (norm_estimate/total_street));
      pDMs[2] = 1 - Math.abs(diffs[2]);
      
      //Estimate P(M|D)
      //uniform
      pMDs[0] = pMs[0]*pDMs[0];
      pMDs[1] = pMs[1]*pDMs[1];
      pMDs[2] = pMs[2]*pDMs[2];
      
      
      // Surprise is the sum of KL divergance across model space
      // Each model also gets a weighted "vote" on what the sign should be
      kl = 0;
      var voteSum = 0;
      for(var j=0;j<pMDs.length;j++){
        kl+= pMDs[j] * (Math.log( pMDs[j] / pMs[j])/Math.log(2));
        voteSum += diffs[j]*pMs[j];
        sumDiffs[j]+=Math.abs(diffs[j]);
      }
      
      surpriseData[prop][i] = voteSum >= 0 ? Math.abs(kl) : -1*Math.abs(kl);

      uniformData[prop][i] = pMs[0];
      baseData[prop][i] = pMs[1];
    }
    
    //Now lets globally update our model belief.
    
    for(var j = 0;j<pMs.length;j++){
      pDMs[j] = 1 - 0.5*sumDiffs[j];
      pMDs[j] = pMs[j]*pDMs[j];
      pMs[j] = pMDs[j];
    }
    
    //Normalize
    var sum = pMs.reduce(function(a, b) { return a + b; }, 0);
    for(var j = 0;j<pMs.length;j++){
      pMs[j]/=sum;
    }
    
    uniform.pM.push(pMs[0]);
    boom.pM.push(pMs[1]);
    bust.pM.push(pMs[2]);
    
  }
  
}

