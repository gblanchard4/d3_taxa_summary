#!/usr/bin/env python

import argparse
import os
import csv
import json
import glob

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"

'''
Make pretty taxa summaries
'''
d3 = """
<!DOCTYPE html>
<meta charset="utf-8">
<head>
    <script src="d3.js"></script>
    <style>
    
        body {
          font: 10px sans-serif;
        }

        h1 {
            font: 20px sans-serif;            
        }
    
        .axis path,
        .axis line {
          fill: none;
          stroke: #000;
          shape-rendering: crispEdges;
        }
    
        .x.axis path {
          display: none;
        }

        .tooltip{
            font-family: sans-serif;
            font-size: 15px;
            font-weight: bold;
            fill:black; 
        }
        
        .node.active {
          fill: blue;
        }

        table {
                border-collapse: collapse;
                border: 2px black solid;
                font: 12px sans-serif;
            }

            td {
                border: 1px black solid;
                padding: 5px;
            }
        
    </style>
</head>
<body>
    <div id="l1">
        <p><h1>Kingdom</h1></p>
    </div>
    <div id="l2">
        <p><h1>Phylum</h1></p>
    </div>
    <div id="l3">
        <p><h1>Class</h1></p>
    </div>
    <div id="l4">
        <p><h1>Order</h1></p>
    </div>
    <div id="l5">
        <p><h1>Family</h1></p>
    </div>
    <div id="l6">
        <p><h1>Genus</h1></p>
    </div>
    <div id="l7">
        <p><h1>Species</h1></p>
    </div>


<script>
    function graph_taxa(file_string, level) {
        d3.csv(file_string, function(error, data) {

            if (error) throw error && hide(level);


            function hide(id){
                d3.select(id).style("visibility","hidden");
            };

            var margin = {top: 25, right: 20, bottom: 20, left: 20},
            w = 960 - margin.left - margin.right,
            h = 500 - margin.top - margin.bottom;

            var x = d3.scale.ordinal()
                .rangeRoundBands([0, w], .1);

            var y = d3.scale.linear()
                .rangeRound([h,0]);

            var xScale = d3.scale.ordinal()
                .rangeRoundBands([0, w], .1);

            var yScale = d3.scale.linear()
                .rangeRound([h, 0]);

            var color = d3.scale.category20b();

            var xAxis = d3.svg.axis()
                .scale(x)
                .orient("bottom");

            var yAxis = d3.svg.axis()
                .scale(y)
                .orient("left")
                .tickFormat(d3.format(".1%"));

            var svg = d3.select(level).append("svg")
                .attr("width", w + margin.left + margin.right)
                .attr("height", h + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            color.domain(d3.keys(data[0]).filter(function(key) { return key !== "SampleID"; }));

            data.forEach(function(d) {
                var sample = d.SampleID;
                var y0 = 0;
                d.taxa = color.domain().map(function(name) { return {sample:sample, name: name, y0: y0, y1: y0 += +d[name]}; });
                d.total = d.taxa[d.taxa.length - 1].y1;

            });

            data.sort(function(a, b) { return b.total - a.total; });

            x.domain(data.map(function(d) { return d.SampleID; }));
            y.domain([0, d3.max(data, function(d) { return d.total; })]);

            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + h + ")")
                .call(xAxis);

            var sample = svg.selectAll(".sample")
                .data(data)
                .enter().append("g")
                .attr("class", "g")
                .attr("transform", function(d) { return "translate(" + x(d.SampleID) + ",0)"; });

            sample.selectAll("rect")
                .data(function(d) { return d.taxa; })
                .enter().append("rect")
                .attr("width", x.rangeBand())
                .attr("y", function(d) { return y(d.y1); })
                .attr("height", function(d) { return y(d.y0) - y(d.y1); })
                .style("fill", function(d) { return color(d.name); })
                .attr("class",function(d){ return d.name; })
                
                .on('mouseover', function (d) {
                    // Show up top
                    var yPos = -10
                    var height = parseFloat(d3.select(this).attr("height"));
                    // Level
                    var levelselect = d3.select(level);


              
                    levelselect.selectAll('.'+d.name).style("opacity","0.55").attr("stroke","yellow").attr("stroke-width",0.8);
                    d3.select(this).attr("stroke","blue").attr("stroke-width",0.8);

                    svg.append("text")
                        // .attr("x",xPos)
                        .attr("y",yPos)
                        .attr("class","tooltip")
                        .attr("text-anchor", "start")
                        .text(d.name);
                })
                .on('mouseout', function (d) {
                    svg.select(".tooltip").remove();
                    //d3.select(this).attr("stroke","pink").attr("stroke-width",0.2);
                    d3.selectAll('.'+d.name).style("opacity", "1").attr("stroke","pink").attr("stroke-width",0.2);
                });

    });
}
"""

# Need to format the filtered tables
def read_summary_file(taxa_file):
	# Filename
	level = taxa_file.lstrip('filtered_').rstrip('.txt')
	dict_list = []
	with open(taxa_file, 'r') as validfile:
		fieldnames = ""
		for line in validfile:
			# Grab header
			if line.startswith('#'):
				fieldnames = line.lstrip('#').rstrip('\n').split('\t')
			else:
				format_line = line.strip('\n').split('\t')
				dict_list.append(dict(zip(header, format_line)))
	return dict_list

# File summary
def read_taxa_files(file_list, category, outdir):
	outfile_dict = {}
	for file in file_list:
		level = os.path.basename(file).split('_L')[1].rstrip('.txt')
		outfile = outdir+'/'+level+'.txt'
		outfile_dict[level] = outfile
		with open(file, 'r') as handle, open(outfile, 'w') as outlevel:
			for line in handle:
				if line .startswith('#'):
					header = line.lstrip('#').rstrip('\n').replace(';','-').replace('[','').replace(']','').split('\t')
					category_pos = header.index(category)
					taxa_pos = header.index("Description")+1
					outlevel.write(header[category_pos]+','+','.join(map(str,header[taxa_pos:]))+'\n')
				else:
					clean_line =  line.rstrip('\n').split('\t')
					outlevel.write(clean_line[category_pos]+','+','.join(map(str,clean_line[taxa_pos:]))+'\n')
	return outfile_dict

def d3_functions(file_dict):
	functions = ""
	i = 1
	while i <= 7:
		if str(i) in file_dict:
			functions += 'graph_taxa("{}",l{})\n'.format(file_dict[str(i)], str(i))
		else:
			functions += 'graph_taxa("{}",l{})\n'.format("NO FILE FOUND", str(i))
		i += 1
	return functions

def main():
	#  Argument Parser
	parser = argparse.ArgumentParser(description='Make pretty taxa summaries using D3')

	# Input file
	parser.add_argument('-i','--input',dest='input', help='The taxa summary folder created with summarize_taxa.py', required=True)
	# Output file
	parser.add_argument('-o','--output',dest='output', help='The output location', required=True)
	# Category
	parser.add_argument('-c','--category', dest='category', help='The category to summarize the taxa by', required=True)

	# Parse arguments
	args = parser.parse_args()
	indir = args.input
	outdir = args.output
	category = args.category

	if not os.path.exists(outdir):
		os.makedirs(outdir)

	file_list = sorted(glob.glob("{}/*_L*.txt".format(indir)))

	taxa_files = read_taxa_files(file_list, category, outdir)

	functions = d3_functions(taxa_files)

	with open('index_test.html', 'w') as html:
		html.write(d3)
		html.write(functions)
		html.write("</script>")


if __name__ == '__main__':
	main()
