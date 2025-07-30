@app.route('/co-locate', methods=['GET', 'POST'])
def colocate():
    if request.method == 'POST':
        try:
            # Collect form data
            project_name = request.form.get('project_name')
            date = request.form.get('date')
            client = request.form.get('client')
            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')
            status = request.form.get('status')
            comments = request.form.get('comments')
            other = request.form.get('other')
            file = request.files.get('file')
            step_number = 1

            conn = get_db_connection()
            with conn.cursor() as cursor:
                # 1. Insert into colocate_project
                cursor.execute("""
                    INSERT INTO colocate_project (project_name, created_at)
                    VALUES (%s, %s)
                """, (project_name, datetime.now()))
                project_id = conn.insert_id()

                # 2. Insert into colocate_step
                cursor.execute("""
                    INSERT INTO colocate_step (
                        project_id, step_number, date, client, person_in_charge,
                        latitude, longitude, status, comment, other
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    project_id, step_number, date, client, 'auto_user',
                    float(latitude) if latitude else 0.0,
                    float(longitude) if longitude else None,
                    status, comments, other
                ))
                step_id = conn.insert_id()

                # 3. Handle file upload (if any)
                if file and file.filename != '':
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)

                    with open(filepath, 'rb') as f:
                        file_blob = f.read()

                    cursor.execute("""
                        INSERT INTO colocate_file (project_id, step_id, file_name, uploaded_at)
                        VALUES (%s, %s, %s, %s)
                    """, (project_id, step_number, file_blob, datetime.now()))

            conn.commit()
            flash("Form submitted successfully!", "success")
        except Exception as e:
            if conn:
                conn.rollback()
            flash(f"Error occurred: {str(e)}", "danger")
        finally:
            if conn:
                conn.close()
        return redirect(url_for('colocate'))

    # GET method: render the form
    return render_template('colocate.html', active_tab='co-locate')