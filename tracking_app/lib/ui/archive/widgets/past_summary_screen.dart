import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import 'package:Snacked/ui/archive/view_model/archive_vm.dart';


class PastSummaryPage extends StatefulWidget {
  const PastSummaryPage({super.key, required this.viewModel});
  final ArchiveViewModel viewModel;

  @override
  State<PastSummaryPage> createState() => _PastSummaryPageState();
}


class _PastSummaryPageState extends State<PastSummaryPage> {

  @override
  Widget build(BuildContext context) {
    return Scaffold (
      appBar: AppBar(
        title: Text('Summary for ${DateFormat('MMMM d, y').format(widget.viewModel.date)}', 
        style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)), backgroundColor: Colors.black),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Column(
                          children: [
                            Text('Eating:', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                            const SizedBox(height:15),
                            Text('${widget.viewModel.eating} min', style: TextStyle(fontSize: 20, color: const Color.fromARGB(255, 39, 183, 255)), textAlign: TextAlign.center),
                          ]
                        ),
                        const SizedBox(width:50),
                        Column(
                          children: [
                            Text('Snacking:', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                            const SizedBox(height:15),
                            Text('${widget.viewModel.snacking} min', style: TextStyle(fontSize: 20, color: Color.fromARGB(255, 39, 183, 255)), textAlign: TextAlign.center),
                          ]
                        )
                      ]
                    ),
                    const SizedBox(height:45),
                    Text('Compared to ${DateFormat('MMM d').format(widget.viewModel.date.subtract(Duration(days:1)))}:', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                    const SizedBox(height:15),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        (widget.viewModel.compIcon && !widget.viewModel.noDiff) ? Text(widget.viewModel.comparison, style: TextStyle(fontSize: 20, color: const Color.fromARGB(255, 66, 255, 72))) 
                        : (widget.viewModel.noDiff ? Text(widget.viewModel.comparison, style: TextStyle(fontSize: 20, fontStyle: FontStyle.italic)) 
                        : Text(widget.viewModel.comparison, style: TextStyle(fontSize: 20, color: Colors.yellow))),
                        const SizedBox(width:5),
                        (widget.viewModel.compIcon && !widget.viewModel.noDiff) ? Icon(Icons.arrow_downward, color: Color.fromARGB(255, 66, 255, 72), size: 20,) 
                        : (widget.viewModel.noDiff ? Icon(Icons.swap_vert, color: Colors.white, size: 20,) 
                        : Icon(Icons.arrow_upward, color: Colors.yellow, size: 20,))
                      ]
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height:15),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  children: [
                    Text('Based on your goals:', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                    const SizedBox(height:15),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        (widget.viewModel.progressIcon) ? Text(widget.viewModel.onTrack, style: TextStyle(fontSize: 20, color: Color.fromARGB(255, 66, 255, 72))) 
                        : Text(widget.viewModel.onTrack, style: TextStyle(fontSize: 20, color: const Color.fromARGB(255, 255, 91, 244))), 
                        const SizedBox(width:10),
                        (widget.viewModel.progressIcon) ? Icon(Icons.thumb_up, color: Color.fromARGB(255, 66, 255, 72), size: 20,) 
                        : Icon(Icons.warning, color: const Color.fromARGB(255, 255, 91, 244), size: 20,)
                      ]
                    ),
                  ]
                ),
              ),
            ),
            const SizedBox(height:15),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  children: [
                    Text('Anything that contributed to snacking?', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                    const SizedBox(height:15),
                    Text(widget.viewModel.comments, style: TextStyle(fontSize: 20, fontStyle: FontStyle.italic), textAlign: TextAlign.center),
                  ]
                ),
              ),
            ),
          ],
        )
      )
    );
  }
}





