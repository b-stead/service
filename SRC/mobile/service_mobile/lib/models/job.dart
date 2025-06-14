class Job {
  final int id;
  final String title;
  final String description;
  final int customerId; // Foreign key for Customer
  final int? createdBy; // Foreign key for created_by (nullable)
  final int? updatedBy; // Foreign key for updated_by (nullable)
  final DateTime startDate;
  final DateTime? endDate; // Nullable
  final String recurrence; // Recurrence type
  final int recurrenceInterval; // Interval for recurrence
  final String status; // Job status
  final DateTime createdAt;
  final DateTime updatedAt;
  final bool isDeleted;
  final DateTime? deletedDate; // Nullable

  Job({
    required this.id,
    required this.title,
    required this.description,
    required this.customerId,
    this.createdBy,
    this.updatedBy,
    required this.startDate,
    this.endDate,
    required this.recurrence,
    required this.recurrenceInterval,
    required this.status,
    required this.createdAt,
    required this.updatedAt,
    required this.isDeleted,
    this.deletedDate,
  });

  // Factory method to parse JSON into a Job object
  factory Job.fromJson(Map<String, dynamic> json) {
    return Job(
      id: json['id'],
      title: json['title'],
      description: json['description'] ?? '',
      customerId: json['customer_id'],
      createdBy: json['created_by'],
      updatedBy: json['updated_by'],
      startDate: DateTime.parse(json['start_date']),
      endDate: json['end_date'] != null ? DateTime.parse(json['end_date']) : null,
      recurrence: json['recurrence'],
      recurrenceInterval: json['recurrence_interval'],
      status: json['status'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
      isDeleted: json['is_deleted'],
      deletedDate: json['deleted_date'] != null ? DateTime.parse(json['deleted_date']) : null,
    );
  }

  // Method to convert a Job object into JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'description': description,
      'customer_id': customerId,
      'created_by': createdBy,
      'updated_by': updatedBy,
      'start_date': startDate.toIso8601String(),
      'end_date': endDate?.toIso8601String(),
      'recurrence': recurrence,
      'recurrence_interval': recurrenceInterval,
      'status': status,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
      'is_deleted': isDeleted,
      'deleted_date': deletedDate?.toIso8601String(),
    };
  }
}